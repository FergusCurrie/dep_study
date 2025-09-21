import { useState } from "react";
import {
  AppBar,
  Toolbar,
  Typography,
  Container,
  Box,
  Paper,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Avatar,
  IconButton,
} from "@mui/material";
import {
  School,
  TrendingUp,
  Assessment,
  Menu,
  Functions,
} from "@mui/icons-material";
import Practice from "./page/Practice.tsx";
import Progress from "./page/Progress.tsx";

function App() {
  const [selectedTab, setSelectedTab] = useState("practice");

  const menuItems = [
    { id: "practice", label: "Practice", icon: <Functions /> },
    { id: "dashboard", label: "Dashboard", icon: <Assessment /> },
    { id: "progress", label: "Progress", icon: <TrendingUp /> },
  ];

  const Sidebar = () => (
    <Box sx={{ width: 250, p: 2 }}>
      <Box sx={{ display: "flex", alignItems: "center", mb: 3 }}>
        <Avatar sx={{ bgcolor: "primary.main", mr: 2 }}>
          <School />
        </Avatar>
        <Typography variant="h6" color="primary">
          Dep practice
        </Typography>
      </Box>
      <List>
        {menuItems.map((item) => (
          <ListItem
            button
            key={item.id}
            selected={selectedTab === item.id}
            onClick={() => {
              setSelectedTab(item.id);
            }}
            // sx={{
            //   borderRadius: 1,
            //   mb: 0.5,
            //   "&.Mui-selected": {
            //     bgcolor: "primary.light",
            //     color: "primary.contrastText",
            //   },
            // }}
          >
            <ListItemIcon
              sx={{
                color:
                  selectedTab === item.id ? "primary.contrastText" : "inherit",
              }}
            >
              {item.icon}
            </ListItemIcon>
            <ListItemText primary={item.label} />
          </ListItem>
        ))}
      </List>
    </Box>
  );

  const renderContent = () => {
    switch (selectedTab) {
      case "dashboard":
        return <Typography variant="h1">Place holder for dashboard</Typography>;
      case "practice":
        return <Practice />;
      case "progress":
        return <Progress />;
      default:
        return <Practice />;
    }
  };

  return (
    <>
      <Box sx={{ display: "flex" }}>
        {/* Sidebar */}
        <Paper
          elevation={1}
          sx={{
            width: 250,
            flexShrink: 0,
            borderRadius: 0,
            borderRight: 1,
            borderColor: "divider",
          }}
        >
          <Sidebar />
        </Paper>

        {/* Main Content */}
        <Box
          component="main"
          sx={{ flexGrow: 1, display: "flex", flexDirection: "column" }}
        >
          {/* App bar */}
          <AppBar position="static" elevation={1}>
            <Toolbar>
              <IconButton edge="start" color="inherit" sx={{ mr: 2 }}>
                <Menu />
              </IconButton>
              <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                Ferg practice
              </Typography>
            </Toolbar>
          </AppBar>
          {/* Conditional render */}
          <Container maxWidth="lg" sx={{ mt: 4, mb: 4, flexGrow: 1 }}>
            {renderContent()}
          </Container>
        </Box>
      </Box>
    </>
  );
}

export default App;
