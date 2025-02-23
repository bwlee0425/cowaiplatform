import React from "react";
import { GoogleLogin } from "@react-oauth/google";

const GoogleAuthButton = () => {
  const handleLoginSuccess = (response) => {
    // 성공적으로 로그인한 경우, response에 포함된 액세스 토큰을 서버로 전송
    const token = response.credential;
    // 서버에 로그인 토큰을 전송하는 로직을 작성합니다.
    fetch("http://your-backend-url/api/auth/google", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ token }),
    })
      .then((res) => res.json())
      .then((data) => {
        // 서버에서 받은 데이터 처리
        console.log(data);
      })
      .catch((error) => {
        console.error("Google login error", error);
      });
  };

  const handleLoginError = () => {
    console.log("Login failed");
  };

  return (
    <div>
      <GoogleLogin
        onSuccess={handleLoginSuccess}
        onError={handleLoginError}
      />
    </div>
  );
};

export default GoogleAuthButton;
