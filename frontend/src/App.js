import React from 'react';

// 'EstrusDashboard' 컴포넌트를 현재 파일에서 임포트합니다.
import EstrusDashboard from './components/EstrusDashboard';

// 'App' 컴포넌트를 정의합니다. 이 컴포넌트는 전체 애플리케이션을 구성하는 핵심 컴포넌트입니다. 애플리케이션의 기본 레이아웃을 정의
function App() {
    // return 구문은 화면에 표시될 JSX를 반환합니다.
    return (
        <div> {/* 이 div 요소는 전체 앱을 감싸는 컨테이너입니다. */}
            {/* 페이지 제목: '한우 AI 발정 감지' */}
            <h1>한우 AI 발정 감지</h1>
            
            {/* EstrusDashboard 컴포넌트를 화면에 표시합니다. */}
            <EstrusDashboard /> {/* 이전에 임포트한 EstrusDashboard 컴포넌트를 화면에 표시합니다. 이 컴포넌트는 실제로 발정 감지 기능을 구현하는 부분입니다. */}
        </div>
    );
}

// App 컴포넌트를 다른 파일에서 사용할 수 있도록 내보냅니다. 이 컴포넌트는 React 애플리케이션의 루트 컴포넌트로 보통 index.js 파일에서 사용됩니다.
export default App;
