import { useState, useEffect } from "react";
import {
  Typography,
  Paper,
} from "@mui/material";
import api from "../api";

interface Review {
  id: number;
  correct: boolean;
  created_date: string;
}

const Progress = () => {
  let [reviews, setReviews] = useState<Array<Review> | null>(null);

  const getReviews = async () => {
    const response = await api.get("/reviews/");
    setReviews(response.data);
  };

  useEffect(() => {
    getReviews();
  }, []);

  return (
    <>
      {reviews && reviews.length > 0 ? (
        <ul>
          {/* 2. Use map to iterate over the array */}
          {reviews.map((review) => (
            <Paper>
              <Typography>{review.id}</Typography>
              <Typography>{review.correct}</Typography>
              <Typography>{review.created_date}</Typography>
            </Paper>
          ))}
        </ul>
      ) : (
        <p>No items to display.</p>
      )}
    </>
  );
};

export default Progress;
