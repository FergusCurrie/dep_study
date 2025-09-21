// import { StrictMode } from 'react'
// import { createRoot } from 'react-dom/client'
// import './index.css'
// import App from './App.tsx'

// createRoot(document.getElementById('root')!).render(
//   <StrictMode>
//     <App />
//   </StrictMode>,
// )


import React from 'react'
import ReactDOM from 'react-dom/client'
import { ThemeProvider, createTheme } from '@mui/material/styles'
import CssBaseline from '@mui/material/CssBaseline'
import App from './App.jsx'
import MarkdownMathRenderer from './components/MarkdownMathRenderer.tsx'

// Create a custom theme (optional)
const theme = createTheme({
  palette: {
    mode: 'light', // or 'dark'
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
  typography: {
    fontFamily: 'Roboto, Arial, sans-serif',
  },
})

//  const sampleContent = `

// ## Inline Math
// Here's Einstein's famous equation: $E = mc^2$,`

//const sampleContent = `The lift coefficient ($C_L$) is a dimensionless coefficient.`
const sampleContent = `Here's Einstein's famous equation: ($E = mc^2$)`

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    
    <ThemeProvider theme={theme}>
      {/* CssBaseline provides consistent baseline CSS across browsers */}
      <CssBaseline />
      <App></App>
    </ThemeProvider>
  </React.StrictMode>,
)