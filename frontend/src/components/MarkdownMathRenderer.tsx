
import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

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

interface MdMathRenderer {
    content: string
}

const MarkdownMathRenderer = (props: MdMathRenderer) => {

  const rehypePlugins = [
    [rehypeKatex, { 
      strict: false,
      throwOnError: false,
      errorColor: '#cc0000',
      output: 'mathml'
    }]
  ];

  return (
    <div>
      <style dangerouslySetInnerHTML={{ __html: katexCSS }} />
      <ReactMarkdown
              remarkPlugins={[remarkMath]}
              rehypePlugins={rehypePlugins}
              components={MarkdownComponents}
            >
              {props.content}
        </ReactMarkdown>
    </div>
  );

}
export default MarkdownMathRenderer;