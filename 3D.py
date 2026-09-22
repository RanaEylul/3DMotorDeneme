<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>3D Araba Motoru Arıza Teşhis Simülasyonu</title>
    <!-- Tailwind CSS ve FontAwesome CDN -->
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Three.js ve OrbitControls -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    <style>
        body { margin: 0; overflow: hidden; background-color: #0f172a; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        #canvas-container { width: 100vw; height: 100vh; display: block; }
        .glow-pulse { animation: pulse 2s infinite; }
        @keyframes pulse {
            0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }
            70% { transform: scale(1.05); box-shadow: 0 0 0 15px rgba(239, 68, 68, 0); }
            100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
        }
    </style>
</head>
<body class="text-white select-none">

    <!-- 3D Canvas Alanı -->
    <div id="canvas-container"></div>

    <!-- Üst Bilgi Paneli -->
    <div class="absolute top-4 left-4 z-10 bg-slate-900/80 backdrop-blur-md p-4 rounded-2xl border border-slate-700 shadow-2xl max-w-sm">
        <h1 class="text-xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-red-500 to-amber-400 flex items-center gap-2">
            <i class="fa-solid fa-car-rear"></i> Motor Arıza Teşhisi
        </h1>
        <p class="text-xs text-slate-300 mt-1">
            Fareyle motoru 360 derece döndür, yakınlaş. Kırmızı yanıp sönen arızalı/eksik parçaların üzerine tıklayarak teşhis et ve onar!
        </p>
        <div class="mt-3 flex items-center justify-between text-xs bg-slate-800/90 p-2 rounded-xl border border-slate-700">
            <span class="text-slate-400">Onarılan Arızalar:</span>
            <span id="score" class="font-bold text-emerald-400 text-sm">0 / 4</span>
        </div>
    </div>

    <!-- Sağ Alt Kontrol İpuçları -->
    <div class="absolute bottom-4 right-4 z-10 bg-slate-900/80 backdrop-blur-md px-4 py-2 rounded-xl border border-slate-700 text-xs text-slate-400 flex items-center gap-3 shadow-lg">
        <span><i class="fa-solid fa-rotate"></i> Döndür: Sol Tık + Sürükle</span>
        <span><i class="fa-solid fa-magnifying-glass"></i> Yakınlaştır: Fare Tekerleği</span>
    </div>

    <!-- Arıza Detay / Onarım Modalı (Gizli Başlangıçta) -->
    <div id="modal" class="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm hidden flex items-center justify-center p-4">
        <div class="bg-slate-900 border border-slate-700 w-full max-w-md rounded-2xl p-6 shadow-2xl relative transform transition-all scale-95 opacity-0" id="modal-content">
            <div class="absolute top-4 right-4 text-slate-400 hover:text-white cursor-pointer text-xl" onclick="closeModal()">
                <i class="fa-solid fa-xmark"></i>
            </div>
            <div class="flex items-center gap-3 mb-4">
                <div class="w-12 h-12 rounded-xl bg-red-500/20 border border-red-500/50 flex items-center justify-center text-red-400 text-xl">
                    <i id="modal-icon" class="fa-solid fa-triangle-exclamation"></i>
                </div>
                <div>
                    <h3 id="modal-title" class="text-lg font-bold text-white">Arıza Başlığı</h3>
                    <span class="text-xs px-2 py-0.5 rounded bg-red-500/20 text-red-400 border border-red-500/30">Kritik Hata</span>
                </div>
            </div>
            <p id="modal-desc" class="text-sm text-slate-300 mb-6 leading-relaxed">
                Arıza açıklaması buraya gelecek.
            </p>
            <div class="flex gap-3">
                <button onclick="closeModal()" class="flex-1 px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-sm font-medium transition">
                    Vazgeç
                </button>
                <button onclick="fixPart()" class="flex-1 px-4 py-2.5 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white text-sm font-semibold shadow-lg shadow-emerald-900/40 transition flex items-center justify-center gap-2">
                    <i class="fa-solid fa-wrench"></i> Parçayı Onar / Değiştir
                </button>
            </div>
        </div>
    </div>

    <!-- Tebrikler / Başarı Ekranı -->
    <div id="success-screen" class="fixed inset-0 z-50 bg-black/80 backdrop-blur-md hidden flex items-center justify-center p-4">
        <div class="bg-slate-900 border border-emerald-500/50 w-full max-w-md rounded-3xl p-8 text-center shadow-2xl shadow-emerald-950/50">
            <div class="w-20 h-20 bg-emerald-500/20 border border-emerald-500/40 rounded-full flex items-center justify-center text-emerald-400 text-3xl mx-auto mb-4 glow-pulse">
                <i class="fa-solid fa-check"></i>
            </div>
            <h2 class="text-2xl font-black text-white mb-2">Tebrikler Usta!</h2>
            <p class="text-slate-300 text-sm mb-6">Araba motorundaki tüm arızaları başarıyla tespit edip onardın. Motor sorunsuz çalışmaya hazır!</p>
            <button onclick="resetSimulation()" class="w-full py-3 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 text-white font-bold text-sm shadow-lg shadow-emerald-900/50 hover:brightness-110 transition">
                Yeniden Başlat
            </button>
        </div>
    </div>

    <script>
        // Three.js Sahne, Kamera ve Renderer Kurulumu
        const container = document.getElementById('canvas-container');
        const scene = new THREE.Scene();
        scene.fog = new THREE.FogExp2(0x0f172a, 0.03);

        const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(0, 5, 12);

        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        renderer.shadowMap.enabled = true;
        container.appendChild(renderer.domElement);

        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        controls.maxPolarAngle = Math.PI / 2 + 0.1; // Yerin altına çok inmesin

        // Işıklandırma (Görünürlüğü artıran modern stüdyo ışıkları)
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
        scene.add(ambientLight);

        const dirLight = new THREE.DirectionalLight(0xffffff, 1.2);
        dirLight.position.set(10, 20, 15);
        dirLight.castShadow = true;
        scene.add(dirLight);

        const blueLight = new THREE.PointLight(0x38bdf8, 2, 50);
        blueLight.position.set(-10, 10, -10);
        scene.add(blueLight);

        // --- ARABA MOTORU MODELİ (Görünür Komponentler) ---
        const engineGroup = new THREE.Group();

        // 1. Motor Ana Blok (Alt Karter ve Gövde)
        const blockGeo = new THREE.BoxGeometry(4, 2.5, 3);
        const blockMat = new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.4, metalness: 0.8 });
        const engineBlock = new THREE.Mesh(blockGeo, blockMat);
        engineBlock.position.y = -0.5;
        engineGroup.add(engineBlock);

        // 2. Silindir Kapağı (Üst Kısım - Metalik Gri)
        const headGeo = new THREE.BoxGeometry(3.8, 1, 2.8);
        const headMat = new THREE.MeshStandardMaterial({ color: 0x94a3b8, roughness: 0.3, metalness: 0.9 });
        const engineHead = new THREE.Mesh(headGeo, headMat);
        engineHead.position.y = 1;
        engineGroup.add(engineHead);

        scene.add(engineGroup);

        // --- ARIZALI / EKSİK PARÇALAR (Etkileşimli Noktalar) ---
        // Her parçaya bir arıza tanımı yüklüyoruz
        const partsData = [
            {
                id: 1,
                name: "Ateşleme Bobini Arızası",
                desc: "3. silindir ateşleme bobini arızalı. Motor tekliyor ve yakıt sarfiyatı artıyor.",
                icon: "fa-bolt",
                position: [-1.2, 1.6, 0.8],
                mesh: null,
                fixed: false
            },
            {
                id: 2,
                name: "Yağ Kaçağı / Filtre Problemi",
                desc: "Yağ filtresi gevşemiş ve contası yırtılmış. Motorda yağ basınç kaybı ve sızıntı var.",
                icon: "fa-oil-can",
                position: [1.5, -0.3, 1.6],
                mesh: null,
                fixed: false
            },
            {
                id: 3,
                name: "Alternatör V Kayışı Kopuk",
                desc: "V kayışı aşınmadan ötürü kopmuş. Akü şarj olmuyor ve direksiyon sertleşiyor.",
                icon: "fa-circle-notch",
                position: [2.1, 0.2, -0.5],
                mesh: null,
                fixed: false
            },
            {
                id: 4,
                name: "Kirlenmiş Hava Filtresi",
                desc: "Hava filtresi tamamen kurum ve tozla tıkanmış. Motor yeterli oksijeni alamıyor.",
                icon: "fa-wind",
                position: [-1.5, 1.2, -1.0],
                mesh: null,
                fixed: false
            }
        ];

        const interactiveMeshes = [];
        const sphereGeo = new THREE.SphereGeometry(0.35, 32, 32);

        partsData.forEach((data) => {
            // Başlangıçta dikkat çeken kırmızı yanıp sönen uyarı küreleri/parçaları
            const mat = new THREE.MeshStandardMaterial({ 
                color: 0xef4444, 
                emissive: 0xef4444, 
                emissiveIntensity: 0.6,
                roughness: 0.2 
            });
            const mesh = new THREE.Mesh(sphereGeo, mat);
            mesh.position.set(...data.position);
            mesh.userData = { id: data.id };
            
            engineGroup.add(mesh);
            data.mesh = mesh;
            interactiveMeshes.push(mesh);
        });

        // Raycaster (Tıklama Algılama)
        const raycaster = new THREE.Raycaster();
        const mouse = new THREE.Vector2();
        let selectedPart = null;

        window.addEventListener('click', (event) => {
            // Sadece canvas alanına tıklandığında çalıştır
            mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
            mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

            raycaster.setFromCamera(mouse, camera);
            const intersects = raycaster.intersectObjects(interactiveMeshes);

            if (intersects.length > 0) {
                const clickedMesh = intersects[0].object;
                const partId = clickedMesh.userData.id;
                const part = partsData.find(p => p.id === partId);

                if (part && !part.fixed) {
                    selectedPart = part;
                    openModal(part);
                }
            }
        });

        // Modal İşlemleri
        const modal = document.getElementById('modal');
        const modalContent = document.getElementById('modal-content');
        
        function openModal(part) {
            document.getElementById('modal-title').innerText = part.name;
            document.getElementById('modal-desc').innerText = part.desc;
            document.getElementById('modal-icon').className = `fa-solid ${part.icon}`;
            
            modal.classList.remove('hidden');
            setTimeout(() => {
                modalContent.classList.remove('scale-95', 'opacity-0');
                modalContent.classList.add('scale-100', 'opacity-100');
            }, 10);
        }

        function closeModal() {
            modalContent.classList.remove('scale-100', 'opacity-100');
            modalContent.classList.add('scale-95', 'opacity-0');
            setTimeout(() => {
                modal.classList.add('hidden');
                selectedPart = null;
            }, 200);
        }

        // Parçayı Onarma Fonksiyonu
        function fixPart() {
            if (!selectedPart) return;

            selectedPart.fixed = true;
            
            // Görseli yeşile çevir ve küçült / sabitle
            selectedPart.mesh.material.color.setHex(0x10b981);
            selectedPart.mesh.material.emissive.setHex(0x10b981);
            selectedPart.mesh.material.emissiveIntensity = 0.2;

            closeModal();
            updateScore();

            // Kontrol et: Tüm arızalar bitti mi?
            if (partsData.every(p => p.fixed)) {
                setTimeout(() => {
                    document.getElementById('success-screen').classList.remove('hidden');
                }, 500);
            }
        }

        let fixedCount = 0;
        function updateScore() {
            fixedCount++;
            document.getElementById('score').innerText = `${fixedCount} / 4`;
        }

        function resetSimulation() {
            location.reload();
        }

        // Animasyon Döngüsü (Hafif motor sarsıntısı ve renk yanıp sönmesi)
        let clock = new THREE.Clock();
        function animate() {
            requestAnimationFrame(animate);

            const elapsedTime = clock.getElapsedTime();

            // Arızalı parçaların kırmızı yanıp sönme efekti
            partsData.forEach(part => {
                if (!part.fixed && part.mesh) {
                    const intensity = 0.4 + Math.sin(elapsedTime * 6) * 0.3;
                    part.mesh.material.emissiveIntensity = intensity;
                }
            });

            controls.update();
            renderer.render(scene, camera);
        }
        animate();

        // Ekran Boyutu Ayarı
        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });
    </script>
</body>
</html>
