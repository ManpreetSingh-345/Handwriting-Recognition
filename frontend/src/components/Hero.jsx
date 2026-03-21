import React, { useState, useEffect } from "react";
import uploadIcon from "../assets/upload-icon.svg";
import axios from "axios";
import Cookies from "js-cookie";

const Hero = () => {
  const [image, setImage] = useState(null);
  axios.defaults.xsrfHeaderName = "X-CSRFToken";
  axios.defaults.xsrfCookieName = "csrftoken";
  axios.defaults.withCredentials = true; // Ensures cookies are sent with cross-site requests

  const handleImage = (event) => {
    if (event.target.files && event.target.files[0]) {
      setImage(event.target.files[0]);
    }
    const formData = new FormData();
    formData.append("image", image);

    axios
      .post("http://localhost:8000/predict/", formData, {
        headers: {
          "X-CSRFToken": Cookies.get("csrftoken"),
        },
      })
      .then((res) => {
        console.log(`Successfully sent. Result: ${res.data}`);
      })
      .catch((error) => {
        console.log(error);
      });
  };
  useEffect(() => {
    const initCSRF = async () => {
      try {
        await axios.get("http://localhost:8000/api/get-csrf/");
        console.log("CSRF Cookie should now be in your DevTools!");
      } catch (err) {
        console.error("Failed to fetch CSRF token", err);
      }
    };
    initCSRF();
  }, []);
  return (
    <section className="relative z-1 flex justify-center items-center font-neue-machina flex-col gap-20">
      <div className="text-4xl">
        Ultimate <span className="text-[#ff5757]">Writing</span> Recognition
      </div>
      {/* Input/Results Section */}
      <div className="bg-[#171717] border border-[#474747] rounded-lg m-5 min-w-xl min-h-50 grid grid-cols-[2fr_1fr] place-items-center divide-x p-5">
        <div>
          <label
            htmlFor="myImage"
            className="py-30 px-50 flex flex-col gap-4 justify-center items-center"
          >
            <img
              src={uploadIcon}
              alt="Upload Icon"
              className="hover:cursor-pointer"
            />
            <div>
              Draw or{" "}
              <span className="underline text-blue-400 bg-[#202020] hover:cursor-pointer">
                upload
              </span>{" "}
              your image here
            </div>
          </label>
          <input
            type="file"
            id="myImage"
            accept="image/*"
            className="hidden"
            onChange={handleImage}
          />

          {image && (
            <img src={URL.createObjectURL(image)} alt="Uploaded Image" />
          )}
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
