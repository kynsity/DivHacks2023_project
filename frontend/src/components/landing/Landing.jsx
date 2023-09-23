import React from "react";
import ROBOT from "../../assets/robot.png"
import STUDENT from "../../assets/student.png"
import BOT from "../../assets/robot_head.png"
import "./landing.css";


export const LandingPage = () => {
  return (
    <div className="landing-page">
      <div className="div">
        <div className="logo">
          <img src={BOT} className="robot-head-img" />
          <p id="logo-text">CiCi</p>
        </div>
        <div className="landing-blurb">
          <p id="main-blurb">
              CS advising made easy.
          </p>
        </div>
        <p id="summary">CS classes are hard. CS advising shouldn't be. Get answers to all your career questions from CiCi!</p>
        <div className="overlap-group">
          <div className="frame" />
          <div className="frame-2" />
          <img src={ROBOT} className="landing-img" />
          <div className="search-bar-2" />
          <div className="search-bar-3" />
          <div className="search-bar-4" />
          <p className="text-wrapper-2">Hi I’m Cici! Let me guide you on your computer science journey!</p>
          <img src={STUDENT} className="student-img" />
          <div className="search-bar-5" />
          <div className="search-bar-6" />
          <p className="text-wrapper-3">What classes should I take?</p>
          <div className="text-wrapper-4">I need help!</div>
        </div>
        
        <div className="text-wrapper-6">ABOUT US</div>
        <div className="div-wrapper">
          <div className="text-wrapper-7">Let’s Talk!</div>
        </div>
        <img src={BOT} className="robot-head-img" />
      </div>
    </div>
  );
};

export default LandingPage