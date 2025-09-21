import { useState, useEffect } from "react";
import { Typography, Button, Box } from "@mui/material";
import MarkdownMathRenderer from "../components/MarkdownMathRenderer.tsx";
import api from "../api";

interface Problem {
  id: number;
  question: string;
  options: string[];
  correct: number;
}

function Practice() {
  const [currentProblem, setCurrentProblem] = useState<Problem | null>(null);
  const [selectedAnswer, setSelectedAnswer] = useState(-1);
  const [showResult, setShowResult] = useState(false);
  const [score, setScore] = useState(0);
  const [problemsAttempted, setProblemsAttempted] = useState(0);

  const getQuestion = async () => {
    const response = await api.get("/api/problems/");
    console.log(response);
    setCurrentProblem(response.data);
  };

  const addReview = async (isCorrect: boolean) => {
    const response = await api.post("/reviews/", {
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

  return (
    <>
      <Box>
        <Box>
          {currentProblem && (
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
                  <Typography variant="body2">
                    {selectedAnswer === currentProblem.correct
                      ? "🎉 Correct! Well done!"
                      : "❌ Incorrect. The correct answer is: " +
                        currentProblem.options[currentProblem.correct]}
                  </Typography>
                </Box>
              )}
            </Box>
          )}
        </Box>
        <Box>
          {!showResult ? (
            <Button
              onClick={handleAnswerSubmit}
              variant="contained"
              disabled={selectedAnswer === null}
            >
              Submit Answer
            </Button>
          ) : (
            <Button onClick={nextProblem} variant="contained">
              Next Problem
            </Button>
          )}
        </Box>
      </Box>
    </>
  );
}

export default Practice;
