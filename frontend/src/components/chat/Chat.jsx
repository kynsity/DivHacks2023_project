import React from "react";
import BOT from "../../assets/robot_head.png"
import "./chat.css";

export const ChatPage = () => {
  return (
    <div className="chat-page">
      <div className="div">
        <div className="overlap-group">
          <div className="border" />
          <div className="text-box-user" />
          <div className="text-box-user-2" />
          <div className="text-box-robot" />
          <div className="text-box-robot-2" />
          <div className="text-wrapper">Hi BitBuddy!!!!!!!</div>
          <p className="p">Hi! I’m BitBuddy, your friendly AI CS advisor.</p>
          <div className="text-wrapper-2">I’m Charlie.</div>
          <div className="text-wrapper-3">How can I help?</div>
          <img className="robot-chat-frame" alt="Robot chat frame" src="robot-chat-frame.svg" />
          <img className="robot-in-chat" alt="Robot in chat" src="robot-in-chat.png" />
          <img src={BOT} className="robot-head-img" />
        </div>
        <div className="overlap">
          <p className="text-wrapper-4">How many credits do I need to graduate?</p>
          <img className="comment" alt="Comment" src="comment-1-1.png" />
        </div>
      </div>
    </div>
  );
};

export default ChatPage