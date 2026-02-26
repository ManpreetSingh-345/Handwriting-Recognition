import React from "react";
import uploadIcon from "./assets/upload-icon.svg";

function App() {
  return (
    <div className="bg-size-[100vh] h-screen bg-black text-white box-border">
      {/* Header */}
      <div className="flex justify-between items-center px-20 py-10 pb-25 font-space-mono">
        <div className=" font-bold text-[38px] text-red-700">SMART WRITE</div>
        <div className="flex justify-between gap-10">
          <button className="hover:cursor-pointer">Dashboard</button>
          <button className="hover:cursor-pointer">API</button>
          <button className="hover:cursor-pointer">Authors</button>
          <button className="hover:cursor-pointer">Contact</button>
        </div>
      </div>
      {/* Hero */}
      <div className="flex justify-center items-center font-neue-machina flex-col gap-20">
        <div className="text-4xl">
          Ultimate <span className="text-red-400">Writing</span> Recognition
        </div>
        <div className="border rounded-lg min-w-xl min-h-30 grid grid-cols-[2fr_1fr] place-items-center divide-x">
          <div className="py-20 px-30 flex flex-col gap-4 justify-center items-center">
            <img
              src={uploadIcon}
              alt="Upload Icon"
              className="hover:cursor-pointer"
            />
            <div>Draw or upload your image here</div>
          </div>
          <div>Result</div>
        </div>
      </div>
    </div>
  );
}

export default App;
