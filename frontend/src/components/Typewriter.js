import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';

const Typewriter = ({ text = '', speed = 40 }) => {
  const [displayedText, setDisplayedText] = useState('');

  useEffect(() => {
    setDisplayedText('');
    let currentIndex = 0;
    const interval = setInterval(() => {
      setDisplayedText(prev => prev + text[currentIndex]);
      currentIndex++;
      if (currentIndex >= text.length) {
        clearInterval(interval);
      }
    }, speed);
    return () => clearInterval(interval);
  }, [text, speed]);

  return <ReactMarkdown>{displayedText}</ReactMarkdown>;
};

export default Typewriter;
