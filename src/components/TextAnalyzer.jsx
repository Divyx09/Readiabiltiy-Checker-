import { useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import axios from "axios";

const TextAnalyzer = () => {
  const [text, setText] = useState("");
  const [analysis, setAnalysis] = useState(null);

  const handleAnalyze = async () => {
    if (!text.trim()) return;

    axios.post("http://127.0.0.1:5000/analyze", { text }).then((res) => {
      if (res.status === 200) {
        console.log(res);
        setAnalysis(res.data);
      }
    });
  };

  return (
    <div className='container border shadow-lg mt-5 text-analyzer'>
      <h2 className='text-center mb-4'>Readability Checker</h2>
      <textarea
        className='form-control custom-textarea'
        rows='5'
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder='Enter your text here...'
      ></textarea>
      <button className='btn btn-primary mt-3' onClick={handleAnalyze}>
        Analyze Text
      </button>
      {analysis && (
        <div className='results mt-4 p-3'>
          <h4>Results:</h4>
          <p>
            <strong>Sentences:</strong> {analysis.statistics.sentence_count}
          </p>
          <p>
            <strong>Words:</strong> {analysis.statistics.word_count}
          </p>
          <p>
            <strong>Unique Words:</strong>
            {analysis.statistics.unique_word_count}
          </p>
          <p>
            <strong>Avg. Word Length:</strong>
            {analysis.statistics.average_word_length}
          </p>
          <p>
            <strong>Flesch Reading Ease:</strong>
            {analysis.readability.flesch_reading_ease}
          </p>
          <p>
            <strong>Flesch-Kincaid Grade:</strong>
            {analysis.readability.flesch_kincaid_grade}
          </p>
        </div>
      )}
    </div>
  );
};

export default TextAnalyzer;
