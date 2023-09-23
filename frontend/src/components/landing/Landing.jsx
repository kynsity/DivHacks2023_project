import React from "react";
import ROBOT from "../../assets/robot.png"
import STUDENT from "../../assets/student.png"
import "./landing.css";

export const LandingPage = () => {
  return (
    <div className="landing-page">
      <div className="div">
        <div className="overlap">
          <img className="search-bar" alt="Search bar" src="search-bar.svg" />
          <p className="lorem-ipsum-dolor">
            <span className="text-wrapper">
              Lorem ipsum <br />
            </span>
            <span className="span">dolor sit </span>
          </p>
        </div>
        <p className="p">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.</p>
        <div className="overlap-group">
          <div className="frame" />
          <div className="frame-2" />
          <img src={ROBOT} className="landing-img" />
          <div className="search-bar-2" />
          <div className="search-bar-3" />
          <div className="search-bar-4" />
          <p className="text-wrapper-2">Hi I’m BitBuddy! Let me guide you on your computer science journey!</p>
          <img src={STUDENT} className="student-img" />
          <div className="search-bar-5" />
          <div className="search-bar-6" />
          <p className="text-wrapper-3">What classes should I take?</p>
          <div className="text-wrapper-4">I need help!</div>
        </div>
        <div className="text-wrapper-5">BitBuddy</div>
        <div className="text-wrapper-6">ABOUT US</div>
        <div className="div-wrapper">
          <div className="text-wrapper-7">Let’s Talk!</div>
        </div>
        <img className="robot-head-top" alt="Robot head top" src="robot-head-top.png" />
      </div>
    </div>
  );
};

export default LandingPage