import * as THREE from './utils/three.module.js';
import { OrbitControls } from './utils/OrbitControls.js';
import { leftWirePath, rightWirePath, wirePath } from './utils/path.js';

let Module = null;

let scene, camera, controls, raycaster;
let renderer;
let INTERSECTED;
let light;
const radius = 150;

const bombHeight = 120, bombWidth = 180, bombDepth = 18, borderSize = 5, indentDepth = 10;

let timer, timerText;
const timerWidth = 30, timerHeight = 15, timerDepth = 5;
const timerX = 0.45 * bombWidth/2, timerY = 0.4 * bombHeight/2, timerZ = bombDepth/2 + timerDepth/2;

let timeLeft, serial;
let sequencePressed = "";
const COLOR = [ 0x000000, 0xff0000, 0xffff00, 0x00ff00, 0x0000ff ];
const currentTime = () => `${String(Math.floor(timeLeft/60)).padStart(2, "0")}:${String(timeLeft%60).padStart(2, "0")}`;

let wires, wireObjects = {};
const wireRadius = 0.85;
const wireWidth = 40, wireHeight = 40;
const connectorWidth = 3, connectorHeight = wireHeight, connectorDepth = 5;
const wireX = -0.4 * bombWidth/2, wireY = 0.4 * bombHeight/2, wireZ = bombDepth/2 + connectorDepth/2;

let seqBtns, seqBtnObjects = {};
const seqBtnWidth = 35, seqBtnHeight = 35, seqBtnDepth = 6;
const btnCapBevel = 2, btnCapGap = 5, btnTravelDepth = 3;
const btnCapSize = (seqBtnWidth-btnCapGap)/2;
const seqBtnX = -0.4 * bombWidth/2, seqBtnY = -0.4 * bombHeight/2, seqBtnZ = bombDepth/2;

let condBtn;
const condBtnRadius = 18, condBtnDepth = 7, condBtnTravelDepth = 6;
const geoRadius = ( Math.pow(condBtnDepth, 2) + Math.pow(condBtnRadius, 2) ) / ( 2*condBtnDepth ); // R = (d^2 + r^2) / 2d
const geoTheta = Math.asin(condBtnRadius / geoRadius);
const condBtnX = 0.45 * bombWidth/2, condBtnY = -0.4 * bombHeight/2, condBtnZ = bombDepth/2 + condBtnTravelDepth + condBtnDepth - geoRadius;

let stem;
const stemRadius = 12;
const stemX = condBtnX, stemY = condBtnY, stemZ = bombDepth/2 + condBtnTravelDepth/2;

let indicatorLight, indicatorLightObj;
const indiRadius = 3, indiDepth = 5;
const indiX = condBtnX + condBtnRadius, indiY = condBtnY + condBtnRadius, indiZ = bombDepth/2 + indiDepth/2;

const pointer = new THREE.Vector2();
const digitalFontUrl = "../static/digital.typeface.json";
let digitalFont;
const loader = new THREE.FontLoader();

function init() {
	scene = new THREE.Scene();
	scene.background = new THREE.Color( 0x303030 );
	camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 2000 );
	camera.position.set( 0, 0, radius );

	renderer = new THREE.WebGLRenderer();
	renderer.setSize( window.innerWidth, window.innerHeight );
	document.body.appendChild( renderer.domElement );
	renderer.shadowMap.enabled = true;
	renderer.shadowMap.type = THREE.PCFSoftShadowMap;
	renderer.outputEncoding = THREE.sRGBEncoding;

	controls = new OrbitControls( camera, renderer.domElement );
	controls.listenToKeyEvents( window );
	controls.enableDamping = true;
	controls.dampingFactor = 0.2;
	controls.screenSpacePanning = false;
	controls.minDistance = 80;
	controls.maxDistance = 200;
	controls.maxPolarAngle = Math.PI;

	light = new THREE.PointLight( 0xffffff, 1, 2000 );
	light.castShadow = true;
	scene.add( light );

	light.shadow.mapSize.width = 1024;
	light.shadow.mapSize.height = 1024;
	light.shadow.camera.far = 1000;
	light.shadow.focus = 1;

	const ambient = new THREE.AmbientLight( 0xffffff, 0.8 );
	scene.add( ambient );

	raycaster = new THREE.Raycaster();

	const bombGeometry = new THREE.BoxGeometry( bombWidth, bombHeight, bombDepth );
	const bombMaterial = new THREE.MeshStandardMaterial({
		color: 0x909090,
		metalness: 0.9,
		roughness: 0.85,
	});
	const base = new THREE.Mesh( bombGeometry, bombMaterial );
	base.receiveShadow = true;
	scene.add( base );

	const borders = [
		{ pos: { x: -bombWidth/2 + borderSize/2, y: 0,           z: bombDepth/2+indentDepth/2 },                  width: borderSize, height: bombHeight },
		{ pos: { x: bombWidth/2 - borderSize/2,  y: 0,           z: bombDepth/2+indentDepth/2 },                  width: borderSize, height: bombHeight },
		{ pos: { x: 0,     						           y: bombHeight/2 - borderSize/2,  z: bombDepth/2+indentDepth/2 }, width: bombWidth, height: borderSize },
		{ pos: { x: 0,     						           y: -bombHeight/2 + borderSize/2, z: bombDepth/2+indentDepth/2 }, width: bombWidth, height: borderSize },
	];

	for (let border of borders) {
		let { pos: {x, y, z}, width, height } = border;
		const borderGeom = new THREE.BoxGeometry( width, height, indentDepth );
		const borderMesh = new THREE.Mesh( borderGeom, bombMaterial );

		borderMesh.position.set( x, y, z );

		borderMesh.castShadow = true;
		borderMesh.receiveShadow = true;
		scene.add( borderMesh );
	}

	const timerGeometry = new THREE.BoxGeometry( timerWidth, timerHeight, timerDepth );
	const timerMaterial = new THREE.MeshBasicMaterial({ color: 0x000000, opacity: 1 });
	timer = new THREE.Mesh( timerGeometry, timerMaterial );

	timer.position.set ( timerX, timerY, timerZ );

	const borderGeometry = new THREE.BoxGeometry( timerWidth+2, timerHeight+2, timerDepth*0.99 );
	const timerBorder = new THREE.Mesh( borderGeometry, bombMaterial );

	timerBorder.position.set( timerX, timerY, timerZ*0.99 );

	timerBorder.castShadow = true;

	scene.add( timerBorder );
	scene.add( timer );

	const connectorGeometry = new THREE.BoxGeometry( connectorWidth, connectorHeight, connectorDepth );
	const connectorMaterial = new THREE.MeshStandardMaterial({
		color: 0x020202,
		metalness: 0.1,
		roughness: 0.7,
	});
	const connectorL = new THREE.Mesh( connectorGeometry, connectorMaterial );
	const connectorR = new THREE.Mesh( connectorGeometry, connectorMaterial );

	connectorL.position.set( wireX - wireWidth/2 + connectorWidth/2, wireY, wireZ );

	connectorR.position.set( wireX + wireWidth/2 + connectorWidth/2, wireY, wireZ );

	connectorL.castShadow = true;
	connectorR.castShadow = true;

	scene.add( connectorL );
	scene.add( connectorR );


	const condBtnColor = 0xff0000;
	const condBtnGeometry = new THREE.SphereGeometry( geoRadius, 32, 8, 0, 2 * Math.PI, 0, geoTheta );
	const condBtnMaterial = new THREE.MeshStandardMaterial({
		color: condBtnColor,
		metalness: 0,
		roughness: 0.4,
	});
	condBtn = new THREE.Mesh( condBtnGeometry, condBtnMaterial );

	condBtn.position.set( condBtnX, condBtnY, condBtnZ );
	condBtn.rotation.x += Math.PI/2;

	condBtn.castShadow = true;
	condBtn.selectable = true;
	condBtn.type = "condition";
	scene.add( condBtn );

	const stemGeometry = new THREE.CylinderGeometry( stemRadius, stemRadius, condBtnTravelDepth, 32 );
	const stemMaterial = new THREE.MeshBasicMaterial({ color: 0x101010 });
	stem = new THREE.Mesh( stemGeometry, stemMaterial );

	stem.position.set( stemX, stemY, stemZ );
	stem.rotation.x += Math.PI / 2;

	stem.castShadow = true;
	scene.add( stem );

	const indiGeometry = new THREE.CylinderGeometry( indiRadius, indiRadius, indiDepth, 16 );
	const indicator = new THREE.Mesh( indiGeometry, bombMaterial );

	indicator.position.set( indiX, indiY, indiZ );
	indicator.rotation.x += Math.PI / 2;

	indicator.castShadow = true;
	scene.add( indicator );

	indicatorLight = new THREE.PointLight( 0x20ff00, 0, 80, 2 );

	const indiObjGeometry = new THREE.SphereGeometry( 0.6*indiRadius, 16, 16 );
	const indiObjMaterial = new THREE.MeshStandardMaterial({
		color: 0x707070,
		metalness: 0.2,
		roughness: 0.4,
		opacity: 0.8,
		transparent: true,
		emissiveIntensity: 3,
	});
	indicatorLightObj = new THREE.Mesh( indiObjGeometry, indiObjMaterial );
	indicatorLight.add( indicatorLightObj );

	indicatorLight.castShadow = true;
	indicatorLight.position.set( indiX, indiY, indiZ + indiDepth/2 );
	scene.add( indicatorLight );

	loader.load( digitalFontUrl, function(font) {
		digitalFont = font;
		setup();
		setSerial(serial);
		renderWires();
		renderSequenceBtns();
	});

	document.addEventListener( 'mousemove', onPointerMove, false );
	document.addEventListener( 'click', onPointerClick, false );
	window.addEventListener( 'resize', onWindowResize );
}

function onWindowResize() {
	camera.aspect = window.innerWidth / window.innerHeight;
	camera.updateProjectionMatrix();
	controls.update();

	renderer.setSize( window.innerWidth, window.innerHeight );
}

function onPointerMove( event ) {
	pointer.x = ( event.clientX / window.innerWidth ) * 2 - 1;
	pointer.y = - ( event.clientY / window.innerHeight ) * 2 + 1;
}

function onPointerClick( event ) {
	if (INTERSECTED == null || !INTERSECTED.selectable) return;

	switch (INTERSECTED.type) {
		case 'wire':
			wires[INTERSECTED.index].cut = true;
			wireObjects[INTERSECTED.index].update = true;
			renderWires();

			const str1 = wires.reduce((arr, el, ind) => (el.cut && arr.push(ind), arr), []).join("");
			const str2 = wires.map(x => x.color).join("");

			Module.ccall("cc", "",
				["string", "number", "string", "number"],
				[str1, str1.length, str2, str2.length]);
			break;
		
		case 'sequence':
			seqBtns[INTERSECTED.index].pressed = true;
			seqBtnObjects[INTERSECTED.index].update = true;
			sequencePressed += String.fromCharCode(65 + INTERSECTED.index);
			renderSequenceBtns();

			Module.ccall("ca", "",
				["string", "number", "number"],
				[sequencePressed, sequencePressed.length, parseInt(serial.substr(2,4), 10)]);
			break;

		case 'condition':
			condBtn.translateY( -condBtnTravelDepth );
			stem.translateY( -condBtnTravelDepth/2 );
			condBtn.selectable = false;
			indicatorLightObj.material.emissive.setHex( 0x00ff00 );
			indicatorLightObj.material.color.set( 0x20ff00 );
			indicatorLight.intensity = 0.8;

			Module.ccall("cb", "",
				["string", "number", "string"],
				[currentTime(), currentTime().length, serial]);
			break;
	
		default:
			break;
	}

	const output = Module.ccall("check", "string", [], []);
	if (output != "") {
		alert(output);
		document.location.reload();
	}
}

function animate() {
	requestAnimationFrame( animate );
	controls.update();
	render();
}

function updateTimer( textContent ) {
	let x = timerX - timerWidth/2, y = timerY - timerHeight/2, z = bombDepth/2 + timerDepth;
	const geometry = new THREE.TextGeometry( textContent, {
		font: digitalFont,
		size: 7,
		height: 0.15,
		curveSegments: 5,
	});
	const material = new THREE.MeshBasicMaterial({ color: 0xff0000 });
	if (timerText != null) scene.remove( timerText );
	timerText = new THREE.Mesh( geometry, material );
	timerText.position.set( x+4, y+4, z );
	scene.add( timerText );
}

function setSerial( textContent ) {
	let x = bombWidth/2, y = -2, z = bombDepth/2;
	const plateThickness = 0.2;
	const geometry = new THREE.TextGeometry( textContent , {
		font: digitalFont,
		size: 5,
		height: 0.15,
		curveSegments: 12,
	});
	const material = new THREE.MeshBasicMaterial({ color: 0x000000 });
	const serial = new THREE.Mesh( geometry, material );
	serial.position.set ( x + plateThickness/2, y, z );

	serial.rotation.y = Math.PI / 2;
	serial.rotation.z = -Math.PI / 2;

	const plateGeometry = new THREE.BoxGeometry(0.2, 32, 8);
	const plateMaterial = new THREE.MeshStandardMaterial({
		metalness: 1,
		roughness: 0.5,
	});
	const plate = new THREE.Mesh( plateGeometry, plateMaterial );
	plate.position.set( x+0.05, y-13, z-2.5 );

	scene.add( serial );
	scene.add( plate );
}

function renderWires() {
	const leftPath = new leftWirePath( wireWidth/3.05 );
	const rightPath = new rightWirePath( wireWidth/3.05 );
	const leftWireGeometry = new THREE.TubeGeometry( leftPath, 8, wireRadius, 12, false );
	const rightWireGeometry = new THREE.TubeGeometry( rightPath, 8, wireRadius, 12, false );
	const path = new wirePath( wireWidth/3.05 );
	const wireGeometry = new THREE.TubeGeometry( path, 8, wireRadius, 12, false );

	for (let i = 0; i < wires.length; i++) {
		let wire = wires[i];

		if ( !wireObjects[i] ) wireObjects[i] = { update: true, mesh: [] };
		if ( !wireObjects[i].update ) continue;
		wireObjects[i].mesh.forEach(x => scene.remove( x ));
		wireObjects[i].update = false;

		const wireMaterial = new THREE.MeshStandardMaterial({
			color: COLOR[wire.color],
			roughness: 0.25,
			metalness: 0
		});
		if ( !wire.cut ) {
			const wireMesh = new THREE.Mesh( wireGeometry, wireMaterial );

			wireMesh.translateX( wireX );
			wireMesh.translateY( wireY - wireHeight * (2*i + 1 - wires.length)/(2*wires.length) );
			wireMesh.translateZ( wireZ );

			wireMesh.castShadow = true;
			wireMesh.selectable = true;
			wireMesh.type = "wire";
			wireMesh.index = i;
			wireObjects[i].mesh.push( wireMesh );
			scene.add( wireMesh );
		} else {
			const leftWireMesh = new THREE.Mesh( leftWireGeometry, wireMaterial );
			const rightWireMesh = new THREE.Mesh( rightWireGeometry, wireMaterial );

			leftWireMesh.translateX( wireX );
			leftWireMesh.translateY( wireY - wireHeight * (2*i + 1 - wires.length)/(2*wires.length) );
			leftWireMesh.translateZ( wireZ );

			rightWireMesh.translateX( wireX );
			rightWireMesh.translateY( wireY - wireHeight * (2*i + 1 - wires.length)/(2*wires.length) );
			rightWireMesh.translateZ( wireZ );

			leftWireMesh.castShadow = true;
			rightWireMesh.castShadow = true;
			wireObjects[i].mesh.push( leftWireMesh );
			wireObjects[i].mesh.push( rightWireMesh );
			scene.add( leftWireMesh );
			scene.add( rightWireMesh );
		}
	}
}

function renderSequenceBtns() {
	const seqBtnShape = new THREE.Shape();
	seqBtnShape.moveTo( -btnCapSize/2, btnCapSize/2 );
	seqBtnShape.lineTo( btnCapSize/2, btnCapSize/2 );
	seqBtnShape.lineTo( btnCapSize/2, -btnCapSize/2 );
	seqBtnShape.lineTo( -btnCapSize/2, -btnCapSize/2 );
	seqBtnShape.lineTo( -btnCapSize/2, btnCapSize/2 );
	const seqBtnGeometry = new THREE.ExtrudeGeometry( seqBtnShape, {
		steps: 1,
		depth: seqBtnDepth,
		bevelEnabled: true,
		bevelThickness: 2,
		bevelSize: btnCapBevel,
		bevelOffset: -btnCapBevel,
		bevelSegments: 1
	});

	const pos = [
		{ x: -seqBtnWidth/2 + btnCapSize/2, y: seqBtnHeight/2 - btnCapSize/2 },
		{ x: seqBtnWidth/2 - btnCapSize/2,  y: seqBtnHeight/2 - btnCapSize/2 },
		{ x: -seqBtnWidth/2 + btnCapSize/2, y: -seqBtnHeight/2 + btnCapSize/2 },
		{ x: seqBtnWidth/2 - btnCapSize/2,  y: -seqBtnHeight/2 + btnCapSize/2 },
	];

	const seqBtnColor = 0x262628;
	for (let i = 0; i < pos.length; i++) {
		const seqBtn = seqBtns[i];

		if ( !seqBtnObjects[i] ) seqBtnObjects[i] = { update: true, mesh: [] };
		if ( !seqBtnObjects[i].update ) continue;
		seqBtnObjects[i].mesh.forEach(x => scene.remove( x ));
		seqBtnObjects[i].update = false;

		const seqBtnMaterial = new THREE.MeshStandardMaterial({
			color: seqBtnColor,
			metalness: 0,
			roughness: 0.9,
		});
		const seqBtnFaceMaterial = new THREE.MeshStandardMaterial({
			color: seqBtnColor,
			metalness: 0,
			roughness: 0.9,
			opacity: 0.7,
			transparent: true,
		});
		const seqBtnMesh = new THREE.Mesh( seqBtnGeometry, [ seqBtnFaceMaterial, seqBtnMaterial ] );

		seqBtnMesh.position.set( seqBtnX + pos[i].x, seqBtnY + pos[i].y, seqBtnZ - 2 - (seqBtn.pressed ? btnTravelDepth : 0) );
		seqBtnMesh.castShadow = true;

		seqBtnMesh.selectable = !seqBtn.pressed;
		seqBtnMesh.type = "sequence";
		seqBtnMesh.index = i;
		seqBtnObjects[i].mesh.push( seqBtnMesh );
		scene.add( seqBtnMesh );

		if ( seqBtn.pressed ) {
			const btnLight = new THREE.PointLight( 0x30ff00, 12, btnCapSize, 2 );
			btnLight.position.set( seqBtnMesh.position.x, seqBtnMesh.position.y, seqBtnMesh.position.z + seqBtnDepth + 2 );
			btnLight.castShadow = true;
			seqBtnObjects[i].mesh.push( btnLight );
			scene.add( btnLight );
		}
		
		const geometry = new THREE.TextGeometry( String.fromCharCode(65 + i), {
			font: digitalFont,
			size: 7,
			height: 0.12,
			curveSegments: 1,
		});
		const material = new THREE.MeshBasicMaterial({ color: 0x000000 });
		const text = new THREE.Mesh( geometry, material );
		text.position.set( seqBtnMesh.position.x - 2, seqBtnMesh.position.y - 3, seqBtnMesh.position.z + seqBtnDepth + btnCapBevel );

		seqBtnObjects[i].mesh.push( text );
		scene.add( text );
	}
}

function setup() {
	const randomLetter = () => String.fromCharCode(65 + Math.floor(Math.random()*6));
	serial = randomLetter() + randomLetter() + Math.floor(Math.random() * 10000).toString().padStart(4, "0") + randomLetter() + randomLetter();

	wires = [];
	const wireCount = 3 + Math.floor(Math.random()*3);

	for (let i = 0; i < wireCount; i++) {
		wires.push({ cut: false, color: Math.floor(Math.random()*5) });
	}

	seqBtns = [
		{ pressed: false },
		{ pressed: false },
		{ pressed: false },
		{ pressed: false },
	];

	timeLeft = 300;
	let counter = setInterval(() => {
		if (timeLeft < 0) {
			clearInterval(counter);
			alert("Obviously a bomb detonates when the timer hits 0 right? What else were you expected :P");
			document.location.reload();
			return;
		}
		timeLeft--;
		updateTimer(currentTime());
	}, 1000);
}

function render() {
	let { x, y, z } = camera.position;
	light.position.set( x + 100, y + 80, z + 80 );

	raycaster.setFromCamera( pointer, camera );

	const intersects = raycaster.intersectObjects( scene.children ).filter(x => x.object.selectable);

	if ( intersects.length > 0 ) {
		if ( INTERSECTED != intersects[ 0 ].object ) {
			if ( INTERSECTED ) {
				INTERSECTED.material instanceof Array
					? INTERSECTED.material.forEach(x => x.emissive?.setHex( INTERSECTED.currentHex ))
					: INTERSECTED.material.emissive?.setHex( INTERSECTED.currentHex );
			}
			INTERSECTED = intersects[ 0 ].object;
			const color = 0x9d9d9d;
			if ( INTERSECTED.material instanceof Array ) {
				INTERSECTED.currentHex = INTERSECTED.material[0].emissive?.getHex();
				INTERSECTED.material.forEach(x => x.emissive?.setHex( color ))
			} else {
				INTERSECTED.currentHex = INTERSECTED.material.emissive?.getHex();
				INTERSECTED.material.emissive?.setHex( color );
			}

			document.body.style.cursor = "pointer";
		}
	} else {
		if ( INTERSECTED ) {
			INTERSECTED.material instanceof Array
				? INTERSECTED.material.forEach(x => x.emissive?.setHex( INTERSECTED.currentHex ))
				: INTERSECTED.material.emissive?.setHex( INTERSECTED.currentHex );
		}
		INTERSECTED = null;
		document.body.style.cursor = "default";
	}

	renderer.render( scene, camera );
}

require(['./main.js'], instance => {
	instance().then(loaded => {
		Module = loaded;
		init();
		animate();
	})
});