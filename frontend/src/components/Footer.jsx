import React from "react";
import twitterIcon from "../assets/twitter.png";
import instagramIcon from "../assets/instagram.webp";

const Footer = () => {
  return (
    <footer className="flex bg-[#202020] rounded-3xl p-20 px-60 mt-15">
      <div className="flex-3 flex flex-col gap-5 align-baseline [&_button]:hover:cursor-pointer">
        <div className=" font-bold text-2xl text-[#ff5757] px-4">
          SMART WRITE
        </div>
        <div>
          <button className="ease-in duration-150 hover:bg-gray-800 px-4 py-2 rounded-2xl">
            Home
          </button>
        </div>
        <div>
          <button className="ease-in duration-150 hover:bg-gray-800 px-4 py-2 rounded-2xl">
            Dashboard
          </button>
        </div>
        <div>
          <button className="ease-in duration-150 hover:bg-gray-800 px-4 py-2 rounded-2xl">
            API
          </button>
        </div>
        <div>
          <button className="ease-in duration-150 hover:bg-gray-800 px-4 py-2 rounded-2xl">
            Authors
          </button>
        </div>
        <div>
          <button className="ease-in duration-150 hover:bg-gray-800 px-4 py-2 rounded-2xl">
            Contact
          </button>
        </div>
      </div>
      <div className="flex-1 flex gap-5 place-self-end justify-end *:hover:cursor-pointer">
        <button>
          <img src={twitterIcon} alt="X/Twitter icon" className="h-6 w-6" />
        </button>
        <button>
          <img src={instagramIcon} alt="Instagram icon" className="h-6 w-6" />
        </button>
      </div>
    </footer>
  );
};

export default Footer;
