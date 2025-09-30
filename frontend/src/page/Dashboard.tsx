import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  CircularProgress,
  Alert,
  Divider,
} from '@mui/material';
import {
  Assignment,
  CheckCircle,
  Schedule,
  TrendingUp,
  Warning,
  CalendarToday,
  CalendarMonth,
  CalendarViewWeek,
} from '@mui/icons-material';
import api from '../api';

interface AnalyticsData {
  summary: {
    total_problems: number;
    total_reviews: number;
    overall_accuracy: number;
    average_ease_factor: number;
    problems_due_today: number;
    problems_due_this_week: number;
    problems_due_this_month: number;
    problems_overdue: number;
  };
  problems: Array<{
    problem_id: number;
    problem_name: string;
    total_reviews: number;
    correct_reviews: number;
    ease_factor: number;
    current_interval: number;
    next_review_date: string;
    due_date: string;
    days_until_due: number;
  }>;
  generated_at: string;
}

const Dashboard: React.FC = () => {
  const [data, setData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        setLoading(true);
        const response = await api.get('/api/analytics/');
        setData(response.data);
        setError(null);
      } catch (err) {
        setError('Failed to fetch analytics data');
        console.error('Error fetching analytics:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchAnalytics();
  }, []);

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const getAccuracyColor = (accuracy: number) => {
    if (accuracy >= 80) return 'success';
    if (accuracy >= 60) return 'warning';
    return 'error';
  };

  const getDueStatusChip = (daysUntilDue: number) => {
    if (daysUntilDue < 0) {
      return <Chip label="Overdue" color="error" size="small" />;
    } else if (daysUntilDue === 0) {
      return <Chip label="Due Today" color="warning" size="small" />;
    } else if (daysUntilDue <= 3) {
      return <Chip label={`Due in ${daysUntilDue} days`} color="info" size="small" />;
    } else {
      return <Chip label={`Due in ${daysUntilDue} days`} color="default" size="small" />;
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <Alert severity="error">{error}</Alert>
      </Box>
    );
  }

  if (!data) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <Alert severity="info">No analytics data available</Alert>
      </Box>
    );
  }

  return (
    <Box>
      <Box display="flex" alignItems="center" gap={1}>
        <Typography variant="h4" gutterBottom>
          Dashboard
        </Typography>
        <Chip
          size="small"
          label={import.meta.env.PROD ? 'prd' : 'dev'}
          color={import.meta.env.PROD ? 'primary' : 'default'}
          sx={{ ml: 1 }}
        />
      </Box>
      <Typography variant="body2" color="text.secondary" gutterBottom>
        Last updated: {formatDate(data.generated_at)}
      </Typography>

      {/* Summary Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <Assignment color="primary" sx={{ mr: 2 }} />
                <Box>
                  <Typography color="text.secondary" gutterBottom>
                    Total Problems
                  </Typography>
                  <Typography variant="h4">
                    {data.summary.total_problems}
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <CheckCircle color="success" sx={{ mr: 2 }} />
                <Box>
                  <Typography color="text.secondary" gutterBottom>
                    Overall Accuracy
                  </Typography>
                  <Typography variant="h4" color={`${getAccuracyColor(data.summary.overall_accuracy)}.main`}>
                    {data.summary.overall_accuracy.toFixed(1)}%
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <TrendingUp color="info" sx={{ mr: 2 }} />
                <Box>
                  <Typography color="text.secondary" gutterBottom>
                    Avg Ease Factor
                  </Typography>
                  <Typography variant="h4">
                    {data.summary.average_ease_factor.toFixed(1)}
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <Schedule color="warning" sx={{ mr: 2 }} />
                <Box>
                  <Typography color="text.secondary" gutterBottom>
                    Total Reviews
                  </Typography>
                  <Typography variant="h4">
                    {data.summary.total_reviews}
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Due Dates Overview */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <CalendarToday color="error" sx={{ mr: 2 }} />
                <Box>
                  <Typography color="text.secondary" gutterBottom>
                    Due Today
                  </Typography>
                  <Typography variant="h4" color="error.main">
                    {data.summary.problems_due_today}
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <CalendarViewWeek color="warning" sx={{ mr: 2 }} />
                <Box>
                  <Typography color="text.secondary" gutterBottom>
                    Due This Week
                  </Typography>
                  <Typography variant="h4" color="warning.main">
                    {data.summary.problems_due_this_week}
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <CalendarMonth color="info" sx={{ mr: 2 }} />
                <Box>
                  <Typography color="text.secondary" gutterBottom>
                    Due This Month
                  </Typography>
                  <Typography variant="h4" color="info.main">
                    {data.summary.problems_due_this_month}
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <Warning color="error" sx={{ mr: 2 }} />
                <Box>
                  <Typography color="text.secondary" gutterBottom>
                    Overdue
                  </Typography>
                  <Typography variant="h4" color="error.main">
                    {data.summary.problems_overdue}
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Divider sx={{ my: 3 }} />

      {/* Problems Table */}
      <Typography variant="h5" gutterBottom>
        Problem Details
      </Typography>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Problem</TableCell>
              <TableCell align="right">Reviews</TableCell>
              <TableCell align="right">Accuracy</TableCell>
              <TableCell align="right">Ease Factor</TableCell>
              <TableCell align="right">Interval (days)</TableCell>
              <TableCell align="center">Due Status</TableCell>
              <TableCell>Next Review</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {data.problems.map((problem) => {
              const accuracy = (problem.correct_reviews / problem.total_reviews) * 100;
              return (
                <TableRow key={problem.problem_id}>
                  <TableCell>
                    <Typography variant="body1" fontWeight="medium">
                      {problem.problem_name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                    </Typography>
                  </TableCell>
                  <TableCell align="right">
                    {problem.total_reviews}
                  </TableCell>
                  <TableCell align="right">
                    <Typography color={`${getAccuracyColor(accuracy)}.main`}>
                      {accuracy.toFixed(1)}%
                    </Typography>
                  </TableCell>
                  <TableCell align="right">
                    {problem.ease_factor.toFixed(1)}
                  </TableCell>
                  <TableCell align="right">
                    {problem.current_interval}
                  </TableCell>
                  <TableCell align="center">
                    {getDueStatusChip(problem.days_until_due)}
                  </TableCell>
                  <TableCell>
                    {formatDate(problem.next_review_date)}
                  </TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};

export default Dashboard;
