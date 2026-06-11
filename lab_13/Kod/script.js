import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

const infoDiv = document.getElementById('info');
const canvas = document.getElementById('webgl');

let scene, camera, renderer, controls, clock;
let animatedMesh = null;
let modelRoot = null;

async function init() {
    try {
        // Tworzenie pustego świata 3D z ciemnym tłem oraz licznika czasu do animacji.
        scene = new THREE.Scene();
        scene.background = new THREE.Color(0x050508); 
        clock = new THREE.Clock();

        // Ustawienie perspektywy widoku użytkownika oraz jego początkowej pozycji.
        camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(10, 10, 10);

        // Konfiguracja wyświetlania obrazu, wygładzania krawędzi, kolorów i miękkich cieni.
        renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        renderer.toneMapping = THREE.ACESFilmicToneMapping;
        renderer.toneMappingExposure = 1.2;
        renderer.outputColorSpace = THREE.SRGBColorSpace;
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;

        // Włączenie obracania i przybliżania widoku wokół modelu z efektem płynnego wyhamowania.
        controls = new OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true; 
        controls.dampingFactor = 0.05;
        controls.minDistance = 0.5;
        controls.maxDistance = 100;

        // Dodanie kolorowych osi (XYZ) oraz siatki podłoża ułatwiających orientację w przestrzeni.
        const axesHelper = new THREE.AxesHelper(5);
        scene.add(axesHelper);
        const gridHelper = new THREE.GridHelper(20, 20, 0x00ffcc, 0x444444);
        scene.add(gridHelper);

        // Konfiguracja czterech świateł: ogólnego, głównego (z cieniami), wypełniającego oraz tylnego (neonowego konturu).
        const ambientLight = new THREE.AmbientLight(0xffffff, 1.5);
        scene.add(ambientLight);

        const keyLight = new THREE.DirectionalLight(0xffbb88, 3.5);
        keyLight.position.set(8, 12, 8);
        keyLight.castShadow = true;
        keyLight.shadow.mapSize.width = 2048;
        keyLight.shadow.mapSize.height = 2048;
        scene.add(keyLight);

        const keyLightHelper = new THREE.DirectionalLightHelper(keyLight, 1);
        scene.add(keyLightHelper);

        const fillLight = new THREE.DirectionalLight(0x4477ff, 2.0);
        fillLight.position.set(-8, 4, -4);
        scene.add(fillLight);

        const rimLight = new THREE.DirectionalLight(0x00ffcc, 3.0);
        rimLight.position.set(0, 6, -10);
        scene.add(rimLight);

        const loader = new GLTFLoader();
        const gltf = await loader.loadAsync('biomech13.glb');
        modelRoot = gltf.scene;
        scene.add(modelRoot);

        let meshCount = 0;
        modelRoot.traverse((child) => {
            if (child.isMesh) {
                meshCount++;
                child.castShadow = true;
                child.receiveShadow = true;
                console.log(`Pomyślnie załadowano Mesh: "${child.name}"`);

                if (child.name.toLowerCase().includes('paczki') || child.name.toLowerCase().includes('rose') || child.name.toLowerCase().includes('archnobot')) {
                    animatedMesh = child;
                    console.log(`-> Znaleziono obiekt do animacji: ${child.name}`);
                }
            }
        });

        infoDiv.innerHTML = `Model załadowany!<br>Liczba mesh-y: ${meshCount}`;
        fitCameraToModel(modelRoot);
        window.addEventListener('resize', onWindowResize);

        animate();

    } catch (error) {
        console.error("Błąd zainicjalizowania sceny:", error);
        infoDiv.classList.add('error');
        infoDiv.innerHTML = `<strong>Błąd ładowania sceny!</strong><br>${error.message}<br><small>Sprawdź konsolę F12.</small>`;
    }
}

function fitCameraToModel(rootObject) {
    const box = new THREE.Box3().setFromObject(rootObject);
    const center = box.getCenter(new THREE.Vector3());
    const size = box.getSize(new THREE.Vector3());
    const maxDim = Math.max(size.x, size.y, size.z);
    
    if(maxDim === 0) {
        console.warn("Uwaga: Wykryto model o zerowym rozmiarze. Kamera ustawia się domyślnie.");
        camera.position.set(5, 5, 5);
        controls.target.set(0, 0, 0);
        return;
    }

    const fov = camera.fov * (Math.PI / 180);
    let cameraZ = Math.abs(maxDim / 2 / Math.tan(fov / 2)) * 1.8;

    controls.target.copy(center);
    camera.position.set(center.x + cameraZ * 0.7, center.y + cameraZ * 0.5, center.z + cameraZ * 0.7);
    camera.lookAt(center);
    
    controls.minDistance = maxDim * 0.1;
    controls.maxDistance = maxDim * 10;
    controls.update();
}

// Zapobiega rozciąganiu obrazu podczas zmiany wielkości okna przeglądarki.
function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

function animate() {
    requestAnimationFrame(animate);

    const delta = clock.getDelta();
    const elapsedTime = clock.getElapsedTime();

    if (modelRoot) {
        modelRoot.rotation.y += 0.1 * delta; 
    }

    controls.update();
    renderer.render(scene, camera);
}

window.addEventListener('DOMContentLoaded', init);