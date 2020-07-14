import React from 'react';

const WebcamCapture = ({ onCapture, value }) => {
  return (
    <input type="file" accept="image/*" capture="camera" onChange={e => onCapture(e.target.files[0])}></input>
  );
};

export default WebcamCapture