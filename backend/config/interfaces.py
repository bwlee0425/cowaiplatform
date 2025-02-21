from abc import ABC, abstractmethod

class AIModelHandler(ABC):
    """
    AI 모델을 다루기 위한 인터페이스(추상 클래스).
    AI 모델의 로드(load) 및 예측(predict) 기능을 표준화하기 위해 사용됨.
    """

    @abstractmethod
    def load_model(self, model_path: str):
        """
        모델을 주어진 경로에서 로드하는 메서드.
        구체적인 로직은 상속받은 클래스에서 구현해야 함.
        :param model_path: 모델 파일의 경로
        """
        pass

    @abstractmethod
    def predict(self, data):
        """
        입력 데이터를 기반으로 예측을 수행하는 메서드.
        구체적인 로직은 상속받은 클래스에서 구현해야 함.
        :param data: 예측을 위한 입력 데이터
        """
        pass

"""주요 개념:
ABC (Abstract Base Class): 추상 클래스로, 직접 인스턴스화할 수 없음.
@abstractmethod: 추상 메서드를 정의하는 데 사용됨. 이를 상속받는 모든 클래스는 반드시 해당 메서드를 구현해야 함.
목적: 다양한 AI 모델(PyTorch, TensorFlow, Scikit-Learn 등)을 동일한 인터페이스로 다룰 수 있도록 표준화함."""