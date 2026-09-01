/**
 * Christopher Johnson - Engineering Portfolio
 * Interactive Functionality & 3D WebGL CAD Viewer
 */

document.addEventListener('DOMContentLoaded', () => {
  initNavigation();
  initScrollSpy();
  initLightbox();
});

/* ==========================================================================
   Navigation & Scroll
   ========================================================================== */
function initNavigation() {
  const mobileToggle = document.getElementById('mobile-toggle');
  const navLinks = document.getElementById('nav-links');

  if (mobileToggle && navLinks) {
    mobileToggle.addEventListener('click', () => {
      navLinks.classList.toggle('active');
    });

    // Close mobile menu on link click
    navLinks.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        navLinks.classList.remove('active');
      });
    });
  }

  // Smooth scroll for internal links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const targetId = this.getAttribute('href');
      if (targetId === '#' || !targetId) return;
      const targetElement = document.querySelector(targetId);
      if (targetElement) {
        e.preventDefault();
        const headerOffset = 80;
        const elementPosition = targetElement.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

        window.scrollTo({
          top: offsetPosition,
          behavior: 'smooth'
        });
      }
    });
  });
}

function initScrollSpy() {
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-link[href^="#"]');

  if (!sections.length || !navLinks.length) return;

  function updateActiveLink() {
    let currentSectionId = '';
    const scrollPosition = window.pageYOffset + 120;

    sections.forEach(section => {
      const sectionTop = section.offsetTop;
      const sectionHeight = section.offsetHeight;
      if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
        currentSectionId = section.getAttribute('id');
      }
    });

    navLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href') === `#${currentSectionId}`) {
        link.classList.add('active');
      }
    });
  }

  window.addEventListener('scroll', updateActiveLink, { passive: true });
  updateActiveLink();
}

/* ==========================================================================
   Image Lightbox Modal
   ========================================================================== */
function initLightbox() {
  const modal = document.getElementById('lightbox-modal');
  const modalImg = document.getElementById('lightbox-img');
  const modalCaption = document.getElementById('lightbox-caption');
  const closeBtn = document.getElementById('lightbox-close');

  if (!modal || !modalImg) return;

  const galleryItems = document.querySelectorAll('.gallery-item, .lightbox-trigger');

  galleryItems.forEach(item => {
    item.addEventListener('click', () => {
      const img = item.querySelector('img') || item;
      const src = img.getAttribute('src');
      const caption = item.getAttribute('data-caption') || img.getAttribute('alt') || '';

      modalImg.src = src;
      if (modalCaption) modalCaption.textContent = caption;
      modal.classList.add('active');
      document.body.style.overflow = 'hidden';
    });
  });

  function closeModal() {
    modal.classList.remove('active');
    document.body.style.overflow = '';
  }

  if (closeBtn) closeBtn.addEventListener('click', closeModal);

  modal.addEventListener('click', (e) => {
    if (e.target === modal || e.target === modal.querySelector('.lightbox-content')) {
      closeModal();
    }
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.classList.contains('active')) {
      closeModal();
    }
  });
}

/* ==========================================================================
   3D CAD Viewer (Three.js with Part Show/Hide Toggles)
   ========================================================================== */
window.initCadViewer = function(containerId, modelUrl) {
  const container = document.getElementById(containerId);
  if (!container) return;

  if (typeof THREE === 'undefined' || typeof THREE.GLTFLoader === 'undefined') {
    console.error('Three.js or GLTFLoader not loaded.');
    container.innerHTML = '<div style="padding:40px;text-align:center;color:#94a3b8;">WebGL Viewer requires Three.js libraries.</div>';
    return;
  }

  // Create UI overlay if not existing
  let partsContainer = document.getElementById('cad-parts-list');
  const loadingIndicator = document.getElementById('cad-loading');

  // Scene setup
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x070b12);

  // Grid floor
  const gridHelper = new THREE.GridHelper(200, 20, 0x1e293b, 0x0f172a);
  gridHelper.position.y = -35;
  scene.add(gridHelper);

  // Camera
  const camera = new THREE.PerspectiveCamera(
    45,
    container.clientWidth / container.clientHeight,
    0.1,
    1000
  );
  camera.position.set(110, 80, 130);

  // Renderer
  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: "high-performance" });
  renderer.setSize(container.clientWidth, container.clientHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.2;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  container.appendChild(renderer.domElement);

  // Orbit Controls
  const controls = new THREE.OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.05;
  controls.maxDistance = 400;
  controls.minDistance = 30;
  controls.autoRotate = false;
  controls.autoRotateSpeed = 1.2;

  // Lighting
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.9);
  scene.add(ambientLight);

  const keyLight = new THREE.DirectionalLight(0x00d2ff, 1.8);
  keyLight.position.set(100, 150, 100);
  scene.add(keyLight);

  const fillLight = new THREE.DirectionalLight(0xff9900, 1.2);
  fillLight.position.set(-100, 80, -100);
  scene.add(fillLight);

  const topLight = new THREE.DirectionalLight(0xffffff, 1.4);
  topLight.position.set(0, 200, 0);
  scene.add(topLight);

  // Parts registry
  const partGroups = {};
  const allMeshes = [];
  let modelRoot = null;

  // Load Model
  const loader = new THREE.GLTFLoader();
  loader.load(
    modelUrl,
    (gltf) => {
      modelRoot = gltf.scene;
      
      // Center and scale
      const box = new THREE.Box3().setFromObject(modelRoot);
      const center = box.getCenter(new THREE.Vector3());
      const size = box.getSize(new THREE.Vector3());
      const maxDim = Math.max(size.x, size.y, size.z);
      const scale = 70 / maxDim;
      
      modelRoot.scale.set(scale, scale, scale);
      modelRoot.position.set(-center.x * scale, -center.y * scale, -center.z * scale);
      scene.add(modelRoot);

      // Extract & Classify Parts
      modelRoot.traverse((child) => {
        if (child.isMesh) {
          allMeshes.push(child);
          // Enhance material
          if (child.material) {
            child.material.metalness = 0.35;
            child.material.roughness = 0.45;
            child.material.side = THREE.DoubleSide;
          }

          const rawName = child.name || 'Component';
          let groupKey = 'Other';

          if (/housingcap/i.test(rawName)) groupKey = 'Housing Cap';
          else if (/housing/i.test(rawName)) groupKey = 'Housing Case';
          else if (/your_ring/i.test(rawName)) groupKey = 'Player Ring';
          else if (/opponent_ring/i.test(rawName)) groupKey = 'Opponent Ring';
          else if (/central_ring/i.test(rawName)) groupKey = 'Central Ring';
          else if (/knob/i.test(rawName)) groupKey = 'Control Knobs';
          else if (/tens_shaft|ones_shaft|axlegear|drive/i.test(rawName)) groupKey = 'Shafts & Internal Gears';
          else if (/idler/i.test(rawName)) groupKey = 'Idler Pinions';
          else if (/screw|m2/i.test(rawName)) groupKey = 'Fasteners (M2)';

          if (!partGroups[groupKey]) {
            partGroups[groupKey] = [];
          }
          partGroups[groupKey].push(child);
        }
      });

      if (loadingIndicator) {
        loadingIndicator.style.display = 'none';
      }

      // Populate UI Toggle Buttons
      if (partsContainer) {
        partsContainer.innerHTML = '';

        // Add Quick Action: Hide/Show Outer Housing
        const housingToggleBtn = document.createElement('button');
        housingToggleBtn.className = 'cad-part-btn active';
        housingToggleBtn.textContent = '👁 Toggle Casing';
        housingToggleBtn.style.borderColor = 'var(--accent-orange)';
        housingToggleBtn.addEventListener('click', () => {
          const housingParts = [...(partGroups['Housing Case'] || []), ...(partGroups['Housing Cap'] || [])];
          const isVisible = housingParts.some(p => p.visible);
          housingParts.forEach(p => { p.visible = !isVisible; });
          housingToggleBtn.classList.toggle('active', !isVisible);
          housingToggleBtn.classList.toggle('hidden-part', isVisible);
          
          // Also sync individual buttons
          document.querySelectorAll('[data-group="Housing Case"], [data-group="Housing Cap"]').forEach(b => {
            b.classList.toggle('active', !isVisible);
            b.classList.toggle('hidden-part', isVisible);
          });
        });
        partsContainer.appendChild(housingToggleBtn);

        // Individual Group Buttons
        Object.keys(partGroups).forEach((groupName) => {
          const btn = document.createElement('button');
          btn.className = 'cad-part-btn active';
          btn.setAttribute('data-group', groupName);
          btn.textContent = groupName;

          btn.addEventListener('click', () => {
            const meshes = partGroups[groupName];
            const isVisible = meshes.some(m => m.visible);
            meshes.forEach(m => { m.visible = !isVisible; });
            btn.classList.toggle('active', !isVisible);
            btn.classList.toggle('hidden-part', isVisible);
          });

          partsContainer.appendChild(btn);
        });
      }
    },
    (xhr) => {
      if (loadingIndicator && xhr.total > 0) {
        const percent = Math.round((xhr.loaded / xhr.total) * 100);
        loadingIndicator.textContent = `Loading CAD 3D Model: ${percent}%`;
      }
    },
    (error) => {
      console.error('Error loading CAD model:', error);
      if (loadingIndicator) {
        loadingIndicator.textContent = 'Interactive 3D Preview (Click & drag to rotate)';
      }
    }
  );

  // Resize Handler
  function onResize() {
    if (!container) return;
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.clientWidth, container.clientHeight);
  }
  window.addEventListener('resize', onResize);

  // Animation Loop
  function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
  }
  animate();

  // Expose helper functions on container
  container._resetView = function() {
    camera.position.set(110, 80, 130);
    controls.target.set(0, 0, 0);
    controls.update();
  };

  container._toggleAutoRotate = function() {
    controls.autoRotate = !controls.autoRotate;
    return controls.autoRotate;
  };
};