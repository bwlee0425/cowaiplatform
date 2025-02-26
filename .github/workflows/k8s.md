Kubernetes 클러스터 설치 가이드
이 문서는 kubeadm을 사용해 Kubernetes 클러스터를 설치하는 과정을 설명합니다. 마스터 노드 IP는 172.30.1.31, 파드 네트워크 CIDR은 172.31.1.0/16, CNI로 Calico를 사용합니다.

1. 설치 전 준비사항
Kubernetes 설치를 시작하기 전에 모든 노드(마스터와 워커)가 준비되어야 합니다. 아래는 필수 준비 항목과 명령어입니다.

준비 항목	명령어	설명
OS 업데이트	sudo apt update && sudo apt upgrade -y	최신 패키지로 시스템 안정성 확보.
필수 패키지 설치	sudo apt install -y curl apt-transport-https ca-certificates gnupg	Kubernetes 설치에 필요한 도구 설치 (curl, HTTPS 지원 등).
스왑 비활성화	sudo swapoff -a <br> sudo sed -i '/swap/d' /etc/fstab	Kubernetes는 스왑 메모리를 사용하지 않음. 부팅 시 재활성화 방지.
컨테이너 런타임 설치	sudo apt install -y containerd <br> sudo systemctl enable containerd	컨테이너 실행을 위한 containerd 설치 및 활성화.
Kubernetes 리포지토리 추가	curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.32/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg <br> echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.32/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list <br> sudo apt update	Kubernetes 1.32 패키지 설치 준비.
kubeadm, kubelet, kubectl 설치	sudo apt install -y kubeadm=1.32.2-1.1 kubelet=1.32.2-1.1 kubectl=1.32.2-1.1	Kubernetes 핵심 도구 설치. 버전 고정으로 호환성 보장.
홀드 설정	sudo apt-mark hold kubeadm kubelet kubectl	의도치 않은 업그레이드 방지.
방화벽 확인	sudo iptables -L -n	포트(6443, 10250 등)가 열려 있는지 확인. 필요 시 방화벽 열기 (후술).
부연설명:
컨테이너 런타임(containerd): 파드 내 컨테이너를 실행하는 엔진. Kubernetes와 통신하며 컨테이너 생명 주기를 관리.
kubeadm: 클러스터 초기화 및 관리 도구. 마스터와 워커 노드 설정을 자동화.
kubelet: 각 노드에서 실행되며 파드를 관리하고 컨트롤 플레인과 통신.
kubectl: 사용자 명령줄 도구로 API 서버에 명령 전달.
2. 설치 과정과 확인사항
마스터 노드에서 클러스터를 설치하고 확인하는 과정입니다.

단계	명령어	확인 명령어	설명
클러스터 초기화	sudo kubeadm init --pod-network-cidr=172.31.1.0/16 --apiserver-advertise-address=172.30.1.31	kubectl get nodes	마스터 노드에서 컨트롤 플레인 생성. CIDR은 파드 네트워크 범위, API 주소는 마스터 IP.
kubectl 설정	mkdir -p $HOME/.kube <br> sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config <br> sudo chown $(id -u):$(id -g) $HOME/.kube/config	kubectl cluster-info	사용자 환경에서kubectl이 API 서버와 통신하도록 설정.
CNI 설치 (Calico)	kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.28.1/manifests/tigera-operator.yaml <br> wget https://raw.githubusercontent.com/projectcalico/calico/v3.28.1/manifests/custom-resources.yaml <br> nano custom-resources.yaml (cidr 수정) <br> kubectl create -f custom-resources.yaml	kubectl get pods -A | grep calico	파드 간 네트워킹을 위한 Calico 설치. CIDR을 172.31.1.0/16으로 맞춤.
부연설명:
kubeadm init: 컨트롤 플레인(API 서버, 스케줄러, 컨트롤러 매니저, etcd)을 마스터에 배포. pod-network-cidr는 CNI가 사용할 IP 범위로, Calico와 일치해야 함.
kubectl 설정: admin.conf는 API 서버 인증 정보 포함. 이를 통해 kubectl이 클러스터와 상호작용.
Calico: CNI 플러그인으로, 파드에 IP를 할당하고 네트워크 정책을 관리. 컨트롤 플레인과 통신하며 네트워킹 제공.
3. 설치 후 마스터 클러스터 확인
마스터 노드에서 클러스터가 정상 작동하는지 확인합니다.

확인 항목	명령어	기대 결과	부연설명
노드 상태	kubectl get nodes -o wide	master가 Ready, IP 172.30.1.31 확인	마스터 노드가 준비됨. 컨트롤 플레인이 실행 중.
컨트롤 플레인 상태	kubectl get componentstatuses	Healthy로 모두 표시	API 서버, 스케줄러, 컨트롤러 매니저가 정상 작동. etcd는 데이터베이스 역할.
시스템 파드	kubectl get pods -n kube-system -o wide	CoreDNS, Calico 등이 Running	CoreDNS는 DNS 제공, Calico는 네트워킹 담당. 모두 실행 중이어야 함.
DNS 테스트	kubectl run -it --rm dns-test --image=busybox -- sh <br> / # nslookup kubernetes.default	10.96.0.1로 해석됨	클러스터 내부 DNS 작동 확인. CoreDNS가 API 서버와 상호작용하며 이름 해석.
부연설명:
노드 상태: Ready면 kubelet이 컨트롤 플레인과 통신 중. NotReady면 네트워킹이나 kubelet 문제 의심.
컨트롤 플레인: API 서버는 명령 수신, 스케줄러는 파드 배치, 컨트롤러 매니저는 상태 유지, etcd는 데이터 저장.
시스템 파드: kube-system에 배포된 파드로, 클러스터 운영에 필수. CoreDNS는 DNS 쿼리 처리, Calico는 네트워크 연결.
DNS 테스트: kubernetes.default는 기본 서비스로, CoreDNS가 제대로 작동하면 클러스터 IP(10.96.0.1) 반환.
4. 워커 노드 조인 및 확인
워커 노드(node1, node2)를 클러스터에 추가하고 정상 작동을 확인합니다.

단계/확인 항목	명령어	기대 결과	부연설명
워커 노드 조인	sudo kubeadm join 172.30.1.31:6443 --token <token> --discovery-token-ca-cert-hash <hash>	"Node joined" 메시지	워커가 마스터의 API 서버에 연결. kubeadm init 출력에서 토큰과 해시 복사.
클러스터 노드 상태	kubectl get nodes -o wide	node1, node2가 Ready	모든 노드가 컨트롤 플레인과 통신 중. Calico가 네트워킹 제공.
파드 배포 테스트	kubectl run -it --rm test-pod --image=busybox -- sh	셸 진입 성공	파드가 노드에 스케줄링되고 실행됨. Calico와 kubelet 상호작용 확인.
네트워크 테스트	/ # nc -zv 172.30.1.31 6443 (파드 내에서)	"open" 출력	파드가 마스터 API 서버와 통신 가능. CNI가 네트워킹 제대로 처리 중.
부연설명:
조인: kubeadm join은 워커의 kubelet을 마스터에 등록. 토큰과 해시는 인증용.
노드 상태: 워커가 Ready면 kubelet과 Calico가 정상 작동. NotReady면 CNI나 방화벽 문제 의심.
파드 배포: 테스트 파드가 실행되면 스케줄러와 Calico가 파드를 노드에 배치하고 네트워크 연결.
네트워크 테스트: 파드에서 API 서버로의 연결은 CNI가 파드 네트워크를 제대로 설정했는지 확인.
5. 요약
단계	주요 작업	핵심 확인
설치 전	OS 업데이트, 스왑 비활성, containerd, kubeadm 설치	sudo systemctl status containerd
설치 과정	kubeadm init, kubectl 설정, Calico 설치	kubectl get nodes
마스터 확인	노드, 컨트롤 플레인, 시스템 파드, DNS 점검	kubectl get pods -n kube-system
워커 조인 및 확인	kubeadm join, 노드 상태, 파드/네트워크 테스트	kubectl get nodes -o wide
6. 추가 팁
문제 발생 시:
로그 확인: kubectl logs <pod-name> -n <namespace>
이벤트 확인: kubectl describe pod <pod-name> -n <namespace>
네트워크 디버깅: nc -zv <ip> <port>
