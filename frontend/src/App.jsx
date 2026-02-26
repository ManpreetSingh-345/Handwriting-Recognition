import React from "react";
import uploadIcon from "./assets/upload-icon.svg";
import { GridPattern } from "@/components/ui/grid-pattern";

function App() {
  return (
    <div className="text-white box-border">
      <div className="border-0 bg-background relative flex flex-col gap-10 overflow-hidden p-10 z-0">
        <GridPattern
          width={70}
          height={70}
          x={-1}
          y={-1}
          strokeDasharray={""}
          className="bg-linear-to-b from-20% from-[#111111] to-80% to-[#434343]"
        />
        {/* Header */}
        <div className="relative flex justify-between items-center px-20 py-10 font-space-mono">
          <div className=" font-bold text-[38px] text-[#ff5757]">
            SMART WRITE
          </div>
          <div className="flex justify-between gap-10">
            <button className="hover:cursor-pointer">Dashboard</button>
            <button className="hover:cursor-pointer">API</button>
            <button className="hover:cursor-pointer">Authors</button>
            <button className="hover:cursor-pointer">Contact</button>
          </div>
        </div>
        {/* Hero */}
        <div className="relative z-1 flex justify-center items-center font-neue-machina flex-col gap-20">
          <div className="text-4xl">
            Ultimate <span className="text-[#ff5757]">Writing</span> Recognition
          </div>
          {/* Input/Results Section */}
          <div className="bg-[#171717] border border-[#474747] rounded-lg m-5 min-w-xl min-h-50 grid grid-cols-[2fr_1fr] place-items-center divide-x p-5">
            <div className="py-30 px-50 flex flex-col gap-4 justify-center items-center">
              <img
                src={uploadIcon}
                alt="Upload Icon"
                className="hover:cursor-pointer"
              />
              <div>
                Draw or{" "}
                <a href="" className="underline text-blue-400 bg-[#202020]">
                  upload
                </a>{" "}
                your image here
              </div>
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
      <div className="border-0 bg-background relative flex flex-col gap-10 overflow-hidden p-20 z-0">
        <GridPattern
          width={70}
          height={70}
          x={-1}
          y={-1}
          strokeDasharray={""}
          className="bg-linear-to-t from-20% from-[#111111] to-80% to-[#434343]"
        />
        <div className="relative flex flex-wrap justify-center gap-50 font-neue-machina text-7xl font-bold *:flex *:flex-col *:items-center *:gap-5">
          <div>
            <div>
              97<span className="text-[#ff5757]">%</span>
            </div>
            <div className="text-4xl">ACCURACY</div>
          </div>
          <div>
            <div>
              100<span className="text-[#ff5757]">+</span>
            </div>
            <div className="text-4xl">USERS</div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
