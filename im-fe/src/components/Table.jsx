import React from 'react'
import { Table } from 'antd'

const columns = [
  {
    title: 'QN',
    dataIndex: 'question_number',
    key: 'question_number',
  },
  {
    title: 'Student Result',
    dataIndex: 'result',
    key: 'result',
    render: (v, r) => <p style={{ color: `${r.correct ? 'red' : ''}` }}>{v}</p>
  },
  {
    title: 'Experted Result',
    dataIndex: 'experted_result',
    key: 'experted_result',
  },
];

const ResultTable = ({ results }) => {
  return (
    <Table dataSource={results} columns={columns} />
  )
}

export default ResultTable