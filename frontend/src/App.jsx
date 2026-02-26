import React from "react";
import uploadIcon from "./assets/upload-icon.svg";
import gridBg from "./assets/grid.png";
import { GridPattern } from "@/components/ui/grid-pattern";

function App() {
  return (
    <div className="text-white box-border">
      {/* Header */}

      {/* Hero */}
      <div className="border-0 bg-background relative flex flex-col gap-10 overflow-hidden rounded-lg p-10 z-[-1]">
        <GridPattern
          width={100}
          height={100}
          x={-1}
          y={-1}
          strokeDasharray={""}
          className="bg-linear-to-b from-20% from-[#111111] to-80% to-[#434343]"
        />
        <div className="relative flex justify-between items-center px-20 py-10 font-space-mono">
          <div className=" font-bold text-[38px] text-red-700">SMART WRITE</div>
          <div className="flex justify-between gap-10">
            <button className="hover:cursor-pointer">Dashboard</button>
            <button className="hover:cursor-pointer">API</button>
            <button className="hover:cursor-pointer">Authors</button>
            <button className="hover:cursor-pointer">Contact</button>
          </div>
        </div>
        <div className="relative z-1 flex justify-center items-center font-neue-machina flex-col gap-20">
          <div className="text-4xl">
            Ultimate <span className="text-red-400">Writing</span> Recognition
          </div>
          {/* Input/Results Section */}
          <div className="border rounded-lg m-5 min-w-xl min-h-50 grid grid-cols-[2fr_1fr] place-items-center divide-x">
            <div className="py-30 px-50 flex flex-col gap-4 justify-center items-center">
              <img
                src={uploadIcon}
                alt="Upload Icon"
                className="hover:cursor-pointer"
              />
              <div>Draw or upload your image here</div>
            </div>
            <div className="flex flex-col items-center h-full py-2">
              <div className="flex-1">RESULT</div>
              <div className="flex-1 text-gray-500">
                RESULTS WILL APPEAR HERE
              </div>
              <div>
                <button className="flex-1">View in Dashboard</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
