import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
// Note: In your actual app, you'll need to install and import KaTeX CSS:
// import 'katex/dist/katex.min.css';

// For this demo, we'll add KaTeX CSS via a style tag
const katexCSS = `
.katex {
  font-family: KaTeX_Main, "Times New Roman", serif;
  font-size: 1.21em;
  line-height: 1.2;
  text-indent: 0;
}
.katex-display {
  display: block;
  margin: 1em 0;
  text-align: center;
}
.katex-display .katex {
  display: block;
  text-align: center;
  white-space: nowrap;
}
.katex .base {
  display: inline-block;
}
`;

// Custom components for styling markdown elements (Material-UI style)
const MarkdownComponents = {
  h1: ({ children }) => (
    <h1 style={{ 
      fontSize: '2.5rem', 
      fontWeight: 300, 
      lineHeight: 1.167,
      letterSpacing: '-0.01562em',
      marginTop: '16px',
      marginBottom: '8px',
      color: '#1976d2'
    }}>
      {children}
    </h1>
  ),
  h2: ({ children }) => (
    <h2 style={{ 
      fontSize: '2rem', 
      fontWeight: 300, 
      lineHeight: 1.2,
      letterSpacing: '-0.00833em',
      marginTop: '16px',
      marginBottom: '8px',
      color: '#1976d2'
    }}>
      {children}
    </h2>
  ),
  h3: ({ children }) => (
    <h3 style={{ 
      fontSize: '1.5rem', 
      fontWeight: 400, 
      lineHeight: 1.334,
      letterSpacing: '0em',
      marginTop: '12px',
      marginBottom: '8px',
      color: '#1976d2'
    }}>
      {children}
    </h3>
  ),
  p: ({ children }) => (
    <p style={{ 
      fontSize: '1rem', 
      fontWeight: 400, 
      lineHeight: 1.5,
      letterSpacing: '0.00938em',
      marginBottom: '16px',
      color: 'rgba(0, 0, 0, 0.87)'
    }}>
      {children}
    </p>
  ),
  code: ({ inline, children, ...props }) => (
    inline ? (
      <code
        style={{
          backgroundColor: '#f5f5f5',
          padding: '2px 4px',
          borderRadius: '4px',
          fontFamily: 'Consolas, Monaco, "Andale Mono", "Ubuntu Mono", monospace',
          fontSize: '0.9em'
        }}
        {...props}
      >
        {children}
      </code>
    ) : (
      <pre
        style={{
          backgroundColor: '#f5f5f5',
          padding: '16px',
          borderRadius: '4px',
          overflow: 'auto',
          fontFamily: 'Consolas, Monaco, "Andale Mono", "Ubuntu Mono", monospace',
          fontSize: '0.9em',
          marginBottom: '16px'
        }}
      >
        <code {...props}>{children}</code>
      </pre>
    )
  ),
  blockquote: ({ children }) => (
    <div
      style={{
        borderLeft: '4px solid #1976d2',
        paddingLeft: '16px',
        marginLeft: '8px',
        fontStyle: 'italic',
        backgroundColor: '#fafafa',
        padding: '8px 16px',
        marginBottom: '16px'
      }}
    >
      {children}
    </div>
  ),
  ul: ({ children }) => (
    <ul style={{ paddingLeft: '16px', marginBottom: '16px' }}>
      {children}
    </ul>
  ),
  li: ({ children }) => (
    <li style={{ marginBottom: '4px' }}>
      {children}
    </li>
  )
};

const MarkdownMathRenderer = () => {
  const [content, setContent] = useState('');
  const [livePreview, setLivePreview] = useState(true);
  const [equations, setEquations] = useState([]);

  // Sample markdown content with equations
  const sampleContent = `# Mathematical Equations Demo

## Inline Math
Here's Einstein's famous equation: $E = mc^2$, and the quadratic formula: $x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}$.

## Block Equations

### Calculus
The fundamental theorem of calculus:

$$\\int_a^b f'(x)\\,dx = f(b) - f(a)$$

### Linear Algebra
Matrix multiplication:

$$\\mathbf{C} = \\mathbf{A} \\mathbf{B} = \\sum_{k=1}^{n} a_{ik} b_{kj}$$

### Statistics
The normal distribution:

$$f(x) = \\frac{1}{\\sigma\\sqrt{2\\pi}} e^{-\\frac{1}{2}\\left(\\frac{x-\\mu}{\\sigma}\\right)^2}$$

### Complex Equations
Schrödinger equation:

$$i\\hbar\\frac{\\partial}{\\partial t}\\Psi(\\mathbf{r},t) = \\hat{H}\\Psi(\\mathbf{r},t)$$

## Code and Math Together

Here's some Python code that calculates the derivative:

\`\`\`python
import numpy as np

def derivative(f, x, h=1e-5):
    return (f(x + h) - f(x - h)) / (2 * h)
\`\`\`

And the mathematical definition: $f'(x) = \\lim_{h \\to 0} \\frac{f(x+h) - f(x)}{h}$

## Lists with Math

1. First derivative: $f'(x) = \\frac{df}{dx}$
2. Second derivative: $f''(x) = \\frac{d^2f}{dx^2}$
3. Partial derivative: $\\frac{\\partial f}{\partial x}$

> **Note**: LaTeX syntax is used for all mathematical expressions.
`;

  useEffect(() => {
    setContent(sampleContent);
  }, []);

  // Simulate fetching equations from FastAPI backend
  useEffect(() => {
    const fetchEquations = async () => {
      // This would be your actual API call to FastAPI
      // const response = await fetch('/api/equations');
      // const data = await response.json();
      
      // Mock data for demonstration
      const mockEquations = [
        {
          id: 1,
          title: "Euler's Identity",
          equation: "$e^{i\\pi} + 1 = 0$",
          description: "The most beautiful equation in mathematics"
        },
        {
          id: 2,
          title: "Maxwell's Equations",
          equation: "$$\\nabla \\cdot \\mathbf{E} = \\frac{\\rho}{\\epsilon_0}$$",
          description: "Gauss's law for electricity"
        },
        {
          id: 3,
          title: "Fourier Transform",
          equation: "$$\\hat{f}(\\xi) = \\int_{-\\infty}^{\\infty} f(x) e^{-2\\pi i x \\xi} dx$$",
          description: "Transforms from time domain to frequency domain"
        }
      ];
      
      setEquations(mockEquations);
    };

    fetchEquations();
  }, []);

  const handleSave = async () => {
    // This would save to your FastAPI backend
    // await fetch('/api/content', {
    //   method: 'POST',
    //   headers: { 'Content-Type': 'application/json' },
    //   body: JSON.stringify({ content })
    // });
    
    alert('Content saved! (This would actually save to your FastAPI backend)');
  };

  const insertEquation = (equation) => {
    setContent(prev => prev + '\n\n' + equation);
  };

  const containerStyle = {
    padding: '24px',
    maxWidth: '1400px',
    margin: '0 auto',
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif'
  };

  const gridStyle = {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: '24px',
    marginBottom: '48px'
  };

  const paperStyle = {
    padding: '16px',
    height: '80vh',
    border: '1px solid #e0e0e0',
    borderRadius: '4px',
    backgroundColor: '#fff',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
  };

  const headerStyle = {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '16px'
  };

  const textareaStyle = {
    width: '100%',
    height: 'calc(100% - 80px)',
    border: '1px solid #ccc',
    borderRadius: '4px',
    padding: '8px',
    fontFamily: 'Consolas, Monaco, "Andale Mono", "Ubuntu Mono", monospace',
    fontSize: '14px',
    resize: 'none',
    outline: 'none'
  };

  const buttonStyle = {
    padding: '8px 16px',
    backgroundColor: '#1976d2',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    marginLeft: '8px'
  };

  const cardStyle = {
    border: '1px solid #e0e0e0',
    borderRadius: '4px',
    padding: '16px',
    marginBottom: '16px',
    backgroundColor: '#fff',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
  };

  const cardGridStyle = {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
    gap: '16px',
    marginTop: '16px'
  };

  return (
    <div style={containerStyle}>
      <style dangerouslySetInnerHTML={{ __html: katexCSS }} />
      
      <h1 style={{ 
        fontSize: '3rem', 
        fontWeight: 300, 
        textAlign: 'center',
        marginBottom: '48px',
        color: '#1976d2'
      }}>
        Markdown + Math Equations Demo
      </h1>
      
      <div style={gridStyle}>
        {/* Editor Side */}
        <div style={paperStyle}>
          <div style={headerStyle}>
            <h2 style={{ margin: 0, fontSize: '1.5rem', fontWeight: 400 }}>
              Markdown Editor
            </h2>
            <div>
              <label style={{ marginRight: '16px' }}>
                <input
                  type="checkbox"
                  checked={livePreview}
                  onChange={(e) => setLivePreview(e.target.checked)}
                />
                {' '}Live Preview
              </label>
              <button style={buttonStyle} onClick={handleSave}>
                Save
              </button>
            </div>
          </div>
          
          <textarea
            style={textareaStyle}
            placeholder="Enter your markdown with LaTeX math equations..."
            value={content}
            onChange={(e) => setContent(e.target.value)}
          />
        </div>

        {/* Preview Side */}
        <div style={{...paperStyle, overflow: 'auto'}}>
          <h2 style={{ margin: '0 0 16px 0', fontSize: '1.5rem', fontWeight: 400 }}>
            Live Preview
          </h2>
          <hr style={{ marginBottom: '16px', border: '1px solid #e0e0e0' }} />
          
          {livePreview && (
            <ReactMarkdown
              remarkPlugins={[remarkMath]}
              rehypePlugins={[rehypeKatex]}
              components={MarkdownComponents}
            >
              {content}
            </ReactMarkdown>
          )}
          
          {!livePreview && (
            <p style={{ color: '#666', fontStyle: 'italic' }}>
              Enable live preview to see rendered content
            </p>
          )}
        </div>
      </div>

      {/* Equation Library */}
      <div>
        <h2 style={{ 
          fontSize: '2rem', 
          fontWeight: 300, 
          marginBottom: '24px',
          color: '#1976d2'
        }}>
          Equation Library
        </h2>
        
        <div style={cardGridStyle}>
          {equations.map((eq) => (
            <div key={eq.id} style={cardStyle}>
              <h3 style={{ 
                marginTop: 0, 
                marginBottom: '16px',
                fontSize: '1.25rem',
                fontWeight: 400
              }}>
                {eq.title}
              </h3>
              
              <div style={{ 
                margin: '16px 0', 
                textAlign: 'center',
                minHeight: '60px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}>
                <ReactMarkdown
                  remarkPlugins={[remarkMath]}
                  rehypePlugins={[rehypeKatex]}
                >
                  {eq.equation}
                </ReactMarkdown>
              </div>
              
              <p style={{ 
                color: '#666', 
                fontSize: '0.9rem',
                marginBottom: '16px'
              }}>
                {eq.description}
              </p>
              
              <button 
                style={{
                  ...buttonStyle,
                  marginLeft: 0,
                  fontSize: '0.875rem'
                }}
                onClick={() => insertEquation(eq.equation)}
              >
                Insert
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default MarkdownMathRenderer;