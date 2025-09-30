import { useEffect, useState } from "react";
import { Box, Paper, Typography, Button, Stack } from "@mui/material";
import api from "../api";

interface SuspendedProblem {
  id: number;
  name: string;
  suspended: boolean;
  suspend_reason?: string | null;
  created_date: string;
}

function Suspended() {
  const [items, setItems] = useState<SuspendedProblem[]>([]);
  const [loading, setLoading] = useState(false);

  const load = async () => {
    setLoading(true);
    try {
      const res = await api.get("/api/problems/suspended");
      setItems(res.data || []);
    } finally {
      setLoading(false);
    }
  };

  const unsuspend = async (problemId: number) => {
    await api.post(`/api/problems/${problemId}/unsuspend`);
    await load();
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <Box>
      <Typography variant="h5" sx={{ mb: 2 }}>Suspended problems</Typography>
      {loading && (
        <Typography variant="body2" sx={{ mb: 2 }}>Loading…</Typography>
      )}
      <Stack spacing={2}>
        {items.map((p) => (
          <Paper key={p.id} variant="outlined" sx={{ p: 2 }}>
            <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>{p.name}</Typography>
            {p.suspend_reason && (
              <Typography variant="body2" sx={{ mt: 0.5, color: "text.secondary" }}>
                Reason: {p.suspend_reason}
              </Typography>
            )}
            <Box sx={{ mt: 1.5 }}>
              <Button variant="contained" color="success" onClick={() => unsuspend(p.id)}>
                Unsuspend
              </Button>
            </Box>
          </Paper>
        ))}
        {!loading && items.length === 0 && (
          <Typography variant="body2" color="text.secondary">No suspended problems.</Typography>
        )}
      </Stack>
    </Box>
  );
}

export default Suspended;


