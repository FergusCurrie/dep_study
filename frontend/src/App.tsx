import React, { useState, useEffect } from 'react';
import {
  Typography,
  Button,
  Box,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  IconButton,
} from '@mui/material';
import {
  PlayArrow,
  Close,
} from '@mui/icons-material';
import MarkdownMathRenderer from './components/MarkdownMathRenderer.tsx'
import api from './api'

// Sample practice problems


interface Problem {
  id: number;
  question: string;
  options: string[];
  correct: number;
  category: string;
}



function App() {


  const [practiceDialog, setPracticeDialog] = useState(false);
  const [currentProblem, setCurrentProblem] = useState<Problem | null>(null);
  const [selectedAnswer, setSelectedAnswer] = useState(-1);
  const [showResult, setShowResult] = useState(false);
  const [score, setScore] = useState(0);
  const [problemsAttempted, setProblemsAttempted] = useState(0);

  const getQuestion = async () => {
        const response = await api.get('/')
        // console.log(response)
        setCurrentProblem(response.data.problem)
    }

  useEffect(() => {
    getQuestion()
  }, [])

  const startPractice = () => {
    //const randomProblem = practiceProblems[Math.floor(Math.random() * practiceProblems.length)];
    //setCurrentProblem(randomProblem);
    setSelectedAnswer(-1);
    setShowResult(false);
    setPracticeDialog(true);
  };

  const handleAnswerSubmit = () => {
    if (selectedAnswer === currentProblem?.correct) {
      setScore(score + 1);
    }
    setProblemsAttempted(problemsAttempted + 1);
    setShowResult(true);
  };

  const nextProblem = () => {
    //const randomProblem = practiceProblems[Math.floor(Math.random() * practiceProblems.length)];
    //setCurrentProblem(randomProblem);
    setSelectedAnswer(-1);
    setShowResult(false);
  };
  const sampleContent = `Here's Einstein's famous equation: ($E = mc^2$)`
  const logProb = () => {
    console.log('test')
    console.log(currentProblem)
  }
  return (
    

    <>
      <Button
              variant="contained"
              startIcon={<PlayArrow />}
              onClick={startPractice}
              size="large"
            >
              Quick Practice
            </Button>

      <Button onClick={logProb}>Check problem</Button>

      <Dialog
        open={practiceDialog}
        onClose={() => setPracticeDialog(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>
          Practice Problem
          <IconButton
            onClick={() => setPracticeDialog(false)}
            sx={{ position: 'absolute', right: 8, top: 8 }}
          >
            <Close />
          </IconButton>
        </DialogTitle>
        <DialogContent>
          {currentProblem && (
            <Box>
              <MarkdownMathRenderer content={currentProblem.question}></MarkdownMathRenderer>

              <Box sx={{ mt: 2 }}>
                {currentProblem.options.map((option, index) => (
                  <Box key={index} sx={{ mb: 1 }}>
                    <Button
                      variant={selectedAnswer === index ? "contained" : "outlined"}
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
                <Box sx={{ mt: 2, p: 2, bgcolor: 'grey.50', borderRadius: 1 }}>
                  <Typography variant="body2">
                    {selectedAnswer === currentProblem.correct
                      ? "🎉 Correct! Well done!"
                      : "❌ Incorrect. The correct answer is: " + currentProblem.options[currentProblem.correct]
                    }
                  </Typography>
                </Box>
              )}
            </Box>
          )}
        </DialogContent>
        <DialogActions>
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
        </DialogActions>
      </Dialog>
    </>
  )
}

export default App


