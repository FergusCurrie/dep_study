import { useEffect, useState } from "react";
import { Box, Paper, Typography, Stack, Chip, TextField, Button, IconButton, Dialog, DialogTitle, DialogContent } from "@mui/material";
import { Cancel, Add } from "@mui/icons-material";
import api from "../api";
import MarkdownMathRenderer from "../components/MarkdownMathRenderer.tsx";

interface ProblemItem {
  id: number;
  name: string;
  created_date: string;
  suspended: boolean;
  suspend_reason?: string | null;
  tags: Array<{ id: number; name: string }> | string[];
}

interface DemoProblem {
  id: number;
  question: string;
  options: string[];
  correct: number;
  solution_explanation?: string;
}

function Browse() {
  const [items, setItems] = useState<ProblemItem[]>([]);
  const [newTag, setNewTag] = useState<Record<number, string>>({});
  const [demoOpen, setDemoOpen] = useState(false);
  const [demo, setDemo] = useState<DemoProblem | null>(null);

  const load = async () => {
    const res = await api.get("/api/problems/all");
    setItems(res.data || []);
  };

  useEffect(() => {
    load();
  }, []);

  const toggleSuspend = async (p: ProblemItem) => {
    if (p.suspended) {
      await api.post(`/api/problems/${p.id}/unsuspend`);
    } else {
      await api.post(`/api/problems/${p.id}/suspend`, { reason: p.suspend_reason || null });
    }
    await load();
  };

  const addTag = async (p: ProblemItem) => {
    const tagName = (newTag[p.id] || "").trim();
    if (!tagName) return;
    await api.post(`/api/problems/${p.id}/tags`, { tag_name: tagName });
    setNewTag({ ...newTag, [p.id]: "" });
    await load();
  };

  const removeTag = async (p: ProblemItem, tagName: string) => {
    await api.delete(`/api/problems/${p.id}/tags`, { data: { tag_name: tagName } });
    await load();
  };

  const renderTags = (p: ProblemItem) => {
    const tagList = Array.isArray(p.tags) ? p.tags : [];
    const normalized = tagList.map((t: any) => (typeof t === "string" ? { name: t } : t));
    return (
      <Stack direction="row" spacing={1} sx={{ flexWrap: "wrap" }}>
        {normalized.map((t, idx) => (
          <Chip key={idx} label={t.name} onDelete={() => removeTag(p, t.name)} />
        ))}
      </Stack>
    );
  };

  const openDemo = async (p: ProblemItem) => {
    const res = await api.get(`/api/problems/${p.id}/demo`);
    setDemo(res.data);
    setDemoOpen(true);
  };
  const closeDemo = () => {
    setDemoOpen(false);
    setDemo(null);
  };

  return (
    <Box>
      <Typography variant="h5" sx={{ mb: 2 }}>Browse problems</Typography>
      <Stack spacing={2}>
        {items.map((p) => (
          <Paper key={p.id} variant="outlined" sx={{ p: 2 }}>
            <Stack direction="row" justifyContent="space-between" alignItems="center">
              <Box sx={{ cursor: 'pointer' }} onClick={() => openDemo(p)}>
                <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>{p.name}</Typography>
                <Typography variant="caption" color="text.secondary">ID: {p.id}</Typography>
                {p.suspend_reason && (
                  <Typography variant="body2" sx={{ mt: 0.5 }}>Reason: {p.suspend_reason}</Typography>
                )}
              </Box>
              <Button variant="contained" color={p.suspended ? "success" : "warning"} onClick={() => toggleSuspend(p)}>
                {p.suspended ? "Unsuspend" : "Suspend"}
              </Button>
            </Stack>
            <Box sx={{ mt: 1.5 }}>{renderTags(p)}</Box>
            <Stack direction="row" spacing={1} alignItems="center" sx={{ mt: 1 }}>
              <TextField size="small" placeholder="Add tag" value={newTag[p.id] || ""} onChange={(e) => setNewTag({ ...newTag, [p.id]: e.target.value })} />
              <IconButton color="primary" onClick={() => addTag(p)}>
                <Add />
              </IconButton>
            </Stack>
          </Paper>
        ))}
      </Stack>

      <Dialog open={demoOpen} onClose={closeDemo} fullWidth maxWidth="md">
        <DialogTitle>Demo problem</DialogTitle>
        <DialogContent>
          {demo && (
            <Box sx={{ mt: 1 }}>
              <Typography variant="subtitle1" sx={{ mb: 1 }}>Question</Typography>
              <Box sx={{ mb: 2 }}>
                <MarkdownMathRenderer content={demo.question} />
              </Box>
              <Typography variant="subtitle1" sx={{ mb: 1 }}>Options</Typography>
              <Stack spacing={1} sx={{ mb: 2 }}>
                {demo.options.map((opt, idx) => (
                  <Paper key={idx} variant={idx === demo.correct ? 'elevation' : 'outlined'} sx={{ p: 1 }}>
                    <Typography variant="body2">{opt}</Typography>
                  </Paper>
                ))}
              </Stack>
              {demo.solution_explanation && (
                <>
                  <Typography variant="subtitle1" sx={{ mb: 1 }}>Explanation</Typography>
                  <MarkdownMathRenderer content={demo.solution_explanation} />
                </>
              )}
            </Box>
          )}
        </DialogContent>
      </Dialog>
    </Box>
  );
}

export default Browse;


