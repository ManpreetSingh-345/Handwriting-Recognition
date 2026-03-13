import React from "react";
import { GridPattern } from "./ui/grid-pattern";

const Header = () => {
  return (
    <>
      <GridPattern
        width={70}
        height={70}
        x={-1}
        y={-1}
        strokeDasharray={""}
        className="bg-linear-to-b from-20% from-[#111111] to-80% to-[#434343]"
      />
      <header className="relative flex justify-between items-center px-20 py-10 font-space-mono">
        <div className=" font-bold text-[38px] text-[#ff5757]">SMART WRITE</div>
        <nav className="flex justify-between gap-5">
          <button className="ease-in duration-150 hover:bg-gray-800 hover:cursor-pointer px-4 py-2 rounded-2xl">
            Dashboard
          </button>
          <button className="ease-in duration-150 hover:bg-gray-800 hover:cursor-pointer px-4 py-2 rounded-2xl">
            API
          </button>
          <button className="ease-in duration-150 hover:bg-gray-800 hover:cursor-pointer px-4 py-2 rounded-2xl">
            Authors
          </button>
          <button className="ease-in duration-150 hover:bg-gray-800 hover:cursor-pointer px-4 py-2 rounded-2xl">
            Contact
          </button>
        </nav>
      </header>
    </>
  );
};

export default Header;
