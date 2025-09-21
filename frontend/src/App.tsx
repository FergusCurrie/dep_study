import React, { useState, useEffect } from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Container,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  LinearProgress,
  Box,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Paper,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
  Avatar,
  IconButton,
  Drawer,
  useTheme,
  useMediaQuery
} from '@mui/material';
import {
  School,
  TrendingUp,
  CheckCircle,
  PlayArrow,
  MenuBook,
  Assessment,
  Menu,
  Close,
  Star,
  Timer,
  Functions
} from '@mui/icons-material';

import api from './api'
// const Diag = ({}) => {
  
//   return (
    
//   )
// }

const courses = [
  {
    id: 1,
    title: "Algebra Fundamentals",
    description: "Master the basics of algebraic expressions and equations",
    progress: 75,
    totalLessons: 24,
    completedLessons: 18,
    difficulty: "Beginner",
    category: "Algebra"
  },
  {
    id: 2,
    title: "Geometry Essentials",
    description: "Explore shapes, angles, and spatial relationships",
    progress: 45,
    totalLessons: 20,
    completedLessons: 9,
    difficulty: "Intermediate",
    category: "Geometry"
  },
  {
    id: 3,
    title: "Calculus I",
    description: "Introduction to limits, derivatives, and integrals",
    progress: 30,
    totalLessons: 32,
    completedLessons: 10,
    difficulty: "Advanced",
    category: "Calculus"
  },
  {
    id: 4,
    title: "Statistics & Probability",
    description: "Data analysis and probability theory fundamentals",
    progress: 60,
    totalLessons: 18,
    completedLessons: 11,
    difficulty: "Intermediate",
    category: "Statistics"
  }
];

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
              <Typography variant="h6" gutterBottom>
                {currentProblem.question}
              </Typography>
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


