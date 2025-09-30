import { useState, useEffect } from "react";
import { Typography, Button, Box, Dialog, DialogTitle, DialogContent, DialogActions, TextField } from "@mui/material";
import MarkdownMathRenderer from "../components/MarkdownMathRenderer.tsx";
import api from "../api";

interface Problem {
  id: number;
  question: string;
  options: string[];
  correct: number;
  solution_explanation?: string;
}

function Practice() {
  const [currentProblem, setCurrentProblem] = useState<Problem | null>(null);
  const [selectedAnswer, setSelectedAnswer] = useState(-1);
  const [showResult, setShowResult] = useState(false);
  const [score, setScore] = useState(0);
  const [problemsAttempted, setProblemsAttempted] = useState(0);
  const [noDue, setNoDue] = useState(false);
  const [suspendOpen, setSuspendOpen] = useState(false);
  const [suspendReason, setSuspendReason] = useState("");

  const getQuestion = async () => {
    try {
      const response = await api.get("/api/problems/");
      const data = response.data;
      if (
        data &&
        typeof data.id === "number" &&
        typeof data.question === "string" &&
        Array.isArray(data.options)
      ) {
        setCurrentProblem(data);
        setNoDue(false);
      } else {
        setCurrentProblem(null);
        setNoDue(true);
      }
    } catch (e) {
      setCurrentProblem(null);
      setNoDue(true);
    }
  };

  const addReview = async (isCorrect: boolean) => {
    const response = await api.post("/api/reviews/", {
      problem_id: currentProblem?.id,
      correct: isCorrect,
    });
  };

  useEffect(() => {
    getQuestion();
  }, []);

  const handleAnswerSubmit = () => {
    if (selectedAnswer === currentProblem?.correct) {
      addReview(true);
      setScore(score + 1);
    } else {
      addReview(false);
    }

    setProblemsAttempted(problemsAttempted + 1);
    setShowResult(true);
  };

  const nextProblem = () => {
    getQuestion();
    setSelectedAnswer(-1);
    setShowResult(false);
  };

  const openSuspend = () => {
    setSuspendOpen(true);
  };

  const closeSuspend = () => {
    setSuspendOpen(false);
    setSuspendReason("");
  };

  const suspendProblem = async () => {
    if (!currentProblem) return;
    await api.post(`/api/problems/${currentProblem.id}/suspend`, { reason: suspendReason });
    closeSuspend();
    nextProblem();
  };

  return (
    <>
      <Box>
        <Box>
          {currentProblem && Array.isArray(currentProblem.options) && (
            <Box>
              <MarkdownMathRenderer
                content={currentProblem.question}
              ></MarkdownMathRenderer>

              <Box sx={{ mt: 2 }}>
                {currentProblem.options.map((option, index) => (
                  <Box key={index} sx={{ mb: 1 }}>
                    <Button
                      variant={
                        selectedAnswer === index ? "contained" : "outlined"
                      }
                      fullWidth
                      onClick={() => setSelectedAnswer(index)}
                      disabled={showResult}
                      color={
                        showResult
                          ? index === currentProblem.correct
                            ? "success"
                            : selectedAnswer === index
                            ? "error"
                            : "inherit"
                          : "primary"
                      }
                    >
                      {option}
                    </Button>
                  </Box>
                ))}
              </Box>
              {showResult && (
                <Box sx={{ mt: 2, p: 2, bgcolor: "grey.50", borderRadius: 1 }}>
                  <Typography variant="body2" sx={{ mb: 2 }}>
                    {selectedAnswer === currentProblem.correct
                      ? "🎉 Correct! Well done!"
                      : "❌ Incorrect. The correct answer is: " +
                        currentProblem.options[currentProblem.correct]}
                  </Typography>
                  
                  {currentProblem.solution_explanation && (
                    <Box sx={{ mt: 2 }}>
                      <MarkdownMathRenderer
                        content={currentProblem.solution_explanation}
                      />
                    </Box>
                  )}
                </Box>
              )}
            </Box>
          )}
          {noDue && (
            <Box sx={{ p: 2, mt: 2 }}>
              <Typography variant="h6">No problems due</Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
                All problems are either not due yet or suspended. Check back later.
              </Typography>
            </Box>
          )}
        </Box>
        <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
          {!showResult ? (
            <Button
              onClick={handleAnswerSubmit}
              variant="contained"
              disabled={selectedAnswer === -1 || !currentProblem}
            >
              Submit Answer
            </Button>
          ) : (
            <Button onClick={nextProblem} variant="contained">
              Next Problem
            </Button>
          )}
          {currentProblem && (
            <Button variant="outlined" color="warning" onClick={openSuspend}>
              Suspend
            </Button>
          )}
        </Box>

        <Dialog open={suspendOpen} onClose={closeSuspend} fullWidth maxWidth="sm">
          <DialogTitle>Suspend this problem</DialogTitle>
          <DialogContent>
            <Typography variant="body2" sx={{ mb: 1 }}>
              Add a quick note on what is wrong with this problem (optional).
            </Typography>
            <TextField
              autoFocus
              multiline
              minRows={3}
              fullWidth
              placeholder="Reason or notes"
              value={suspendReason}
              onChange={(e) => setSuspendReason(e.target.value)}
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={closeSuspend}>Cancel</Button>
            <Button onClick={suspendProblem} variant="contained" color="warning">Suspend</Button>
          </DialogActions>
        </Dialog>
      </Box>
    </>
  );
}

export default Practice;
