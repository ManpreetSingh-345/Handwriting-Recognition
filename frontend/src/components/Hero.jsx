import React from "react";
import uploadIcon from "../assets/upload-icon.svg";

const Hero = () => {
  return (
    <section className="relative z-1 flex justify-center items-center font-neue-machina flex-col gap-20">
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
          <div className="flex-1 text-gray-500">RESULTS WILL APPEAR HERE</div>
          <div>
            <button className="flex-1 ease-in duration-150 hover:bg-gray-800 hover:cursor-pointer px-4 py-2 rounded-2xl">
              View in Dashboard
            </button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
