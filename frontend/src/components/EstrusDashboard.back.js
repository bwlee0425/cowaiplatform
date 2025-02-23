import React, { useState } from 'react'; // React와 useState 훅을 가져옵니다.
import axios from 'axios'; // axios는 HTTP 요청을 보내기 위해 사용됩니다.

const EstrusDashboard = () => {
    // result는 발정 감지 결과를 저장하기 위한 상태입니다.
    // 초기 값은 null로 설정되어 있으며, 결과를 저장하게 됩니다.
    const [result, setResult] = useState(null);

    // detectEstrus 함수는 발정 감지 버튼을 클릭했을 때 실행됩니다.
    const detectEstrus = async () => {
        try {
            const dummyData = [1, 2, 3];
            const response = await axios.post('http://localhost:8000/api/v1/estrus/', {
                cow_id: "1", // CharField에 맞춰 문자열로
                // cctv_source: "http://example.com/cctv/video.mp4" // 모델의 cctv_source 필드 사용
            });
            setResult(response.data.prediction);
        } catch (error) {
            console.error("Error:", error.response ? error.response.data : error.message);
            setResult("오류 발생: " + (error.response ? JSON.stringify(error.response.data) : error.message));
        }
    };

    // 컴포넌트의 반환 부분입니다. UI를 정의합니다.
    return (
        <div>
            {/* 발정 감지 버튼을 클릭하면 detectEstrus 함수가 호출됩니다. */}
            <button onClick={detectEstrus}>발정 감지</button>

            {/* 결과가 있을 경우 결과를 화면에 표시합니다. */}
            {result && <p>결과: {JSON.stringify(result)}</p>}
        </div>
    );
};

// 이 컴포넌트를 다른 파일에서 사용할 수 있도록 내보냅니다.
export default EstrusDashboard;


/*주요 부분 설명:
useState 훅:

const [result, setResult] = useState(null);
React에서 상태를 관리할 때 사용합니다. result는 발정 감지 결과를 저장하고, setResult는 그 상태를 업데이트하는 함수입니다. 초기 값은 null로 설정되어 있습니다.
detectEstrus 함수:

이 함수는 사용자가 "발정 감지" 버튼을 클릭할 때 호출됩니다.
dummyData는 CCTV에서 받았다고 가정한 임시 데이터입니다. 실제 데이터는 CCTV에서 실시간으로 받아야 합니다.
axios.post를 사용하여 FastAPI 서버로 HTTP POST 요청을 보냅니다. 이때 cctv_frame 키로 dummyData를 서버에 전달합니다.
서버가 응답을 보내면 그 응답에서 발정 감지 결과(prediction)를 setResult를 사용하여 상태로 업데이트합니다.
렌더링:

버튼을 클릭하면 detectEstrus 함수가 실행됩니다.
result가 존재하면 그 값을 <p>결과: {result}</p>로 화면에 표시합니다. result가 없으면 아무 것도 렌더링되지 않습니다.
코드 흐름:
사용자가 버튼을 클릭합니다.
detectEstrus 함수가 호출되어 서버로 CCTV 데이터를 보냅니다.
서버에서 발정 감지 결과를 받아와서 result 상태를 업데이트합니다.
result가 업데이트되면 화면에 결과가 표시됩니다.*/