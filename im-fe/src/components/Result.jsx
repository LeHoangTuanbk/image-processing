import React from 'react'
import { Modal, Button } from 'antd';

import ResultTable from './Table'

const Result = ({ showModal, result, onCancel, point }) => {
  return (
    <Modal visible={showModal} onCancel={onCancel} onOk={onCancel} title="Result">
      {!result ? <p>Processing...</p> : result.error == 500 ? <p>Error image.</p> : (
        <div>
          <p>Exam ID: {result.examId.join('')}</p>
          <p>Student ID: {result.studentId.join('')}</p>
          <ResultTable results={result.values.map((v, i) => ({
            key: i,
            question_number: `Câu ${i + 1}`,
            result: v,
            experted_result: result.expected_results[i],
            correct: result.wrongs.indexOf(i) != -1,
          }))} />
          <p>Point: {point}/50</p>
        </div>
      )}
    </Modal>
  )

}

export default Result