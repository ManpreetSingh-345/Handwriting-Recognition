import React from "react";
import tabsIcon from "../assets/tabs.png";
import { GridPattern } from "./ui/grid-pattern";

const Metric = () => {
  return (
    <>
      <section className="border-0 bg-background relative flex flex-col gap-10 overflow-hidden p-20 z-0">
        <GridPattern
          width={70}
          height={70}
          x={-1}
          y={-1}
          strokeDasharray={""}
          className="bg-linear-to-t from-black to-50% to-[#434343]"
        />
        {/* Metric Section */}
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
        <article className="relative font-neue-machina p-20 grid grid-cols-2 items-center">
          <div className="flex flex-col gap-5">
            <div className="text-4xl">
              Ease of <span className="underline text-[#ff5757]">Use</span>
            </div>
            <div className="font-space-mono">
              Lorem Ipsum is simply dummy text of the printing and typesetting
              industry. Lorem Ipsum has been the industry's standard dummy text
              ever since the 1500s, when an unknown printer took a galley of
              type and scrambled it to make a type specimen book.
            </div>
          </div>
          <div className="flex justify-center">
            <img src={tabsIcon} alt="Tabs" />
          </div>
        </article>
      </section>
      <section className="bg-radial-[at_80%_90%] from-50% from-[#d42f32] to-70% to-black">
        <article className="flex justify-center py-20">
          <div className="flex flex-col text-center min-w-100 max-w-200 gap-5">
            <div className="text-3xl">
              Developed by{" "}
              <span className="underline text-[#ff5757]">Students</span>
            </div>
            <div className="text-1xl">
              This application was fully developed by students as part of their
              journey toward becoming software engineers. What began as a simple
              idea evolved into a full-fledged application with features and
              design principles aligned with industry standards, demonstrating
              both technical skill and real-world applicability.
            </div>
            <div>
              <button className="ease-in duration-150 hover:text-black hover:bg-white hover:cursor-pointer bg-[#202020] px-5 py-2 rounded-3xl text-sm">
                Authors
              </button>
            </div>
          </div>
        </article>
        <section className="flex flex-col items-center gap-5 bg-radial-[at_80%_-120%] from-50% from-[#d42f32] to-70% to-black pt-20">
          <div className="text-3xl">
            <span className="text-[#ff5757] underline">API</span> Integration
          </div>
          <div>
            Our industry-leading models are designed for real-world utility.
          </div>
          <div className="flex gap-10 text-black text-sm">
            <div className="bg-linear-to-br from-[#fff7ad] to-[#ffa9f9] px-5 pr-20 py-7 rounded-3xl flex flex-col gap-10">
              <div>
                <h1 className="text-4xl font-space-mono pb-5 font-bold">
                  SW-57
                </h1>
                <p>Flagship Model</p>
              </div>
              <div className="flex flex-col gap-3">
                <div>
                  <p>
                    <span className="font-bold">Input:</span> $1.75 per 1M
                    tokens
                  </p>
                  <p>Output: $14.00 per 1M tokens</p>
                </div>
                <div>
                  <p>400K context length</p>
                  <p>128K max output tokens</p>
                </div>
                <div>
                  <p>Knowledge cut-off: Aug 31, 2025</p>
                </div>
              </div>
              <div>
                <button className="text-white bg-black px-3 py-2 rounded-2xl ease-in duration-150 hover:text-black hover:bg-white hover:cursor-pointer">
                  KNOW MORE
                </button>
              </div>
            </div>
            <div className="bg-linear-to-br from-[#ff7c90] to-[#ffe1a4] px-5 pr-20 py-7 rounded-3xl flex flex-col gap-10">
              <div>
                <h1 className="text-4xl font-space-mono pb-5 font-bold">
                  DW-37
                </h1>
                <p>Initial Model</p>
              </div>
              <div className="flex flex-col gap-3">
                <div>
                  <p>Input: $0.25 per 1M tokens</p>
                  <p>Output: $2.00 per 1M tokens</p>
                </div>
                <div>
                  <p>400K context length</p>
                  <p>128K max output tokens</p>
                </div>
                <div>
                  <p>Knowledge cut-off: Sep 30, 2024</p>
                </div>
              </div>
              <div>
                <button className="text-white bg-black px-3 py-2 rounded-2xl ease-in duration-150 hover:text-black hover:bg-white hover:cursor-pointer">
                  KNOW MORE
                </button>
              </div>
            </div>
          </div>
        </section>
      </section>
    </>
  );
};

export default Metric;
