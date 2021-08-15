import * as THREE from './three.module.js';

export class leftWirePath extends THREE.Curve {
	constructor( scale = 1 ) {
		super();
		this.scale = scale;
	}

	getPoint( t, optionalTarget = new THREE.Vector3() ) {
		const tx = 1.4 * t - 1.5;
		const ty = 0.2 * (t > 0.8 ? t - 0.8 : 0) + 0.16 * Math.sin( 3 * Math.PI * t/2 ) + 0.20 * Math.sin( Math.PI / 2 * (t/2 - 5) ) - 0.27 * Math.sin( Math.PI * t/2 ) - 0.09 * Math.sin( 4/7 * Math.PI * (t/2 - 1) ) - 0.11 * Math.cos( 6 * Math.PI * t/2 );
		const tz = t < 0.7 ? 0 : Math.pow(2.1, t) - Math.pow(2.1, 0.7);
		
		return optionalTarget.set( tx, ty, tz ).multiplyScalar( this.scale );
	}
}

export class rightWirePath extends THREE.Curve {
	constructor( scale = 1 ) {
		super();
		this.scale = scale;
	}

	getPoint( t, optionalTarget = new THREE.Vector3() ) {
		const tx = 1.4 * t + 0.25;
		const ty = 0.1 * (t < 0.3 ? t - 0.3 : 0) + 0.16 * Math.sin( 3 * Math.PI * (t/2 + 0.5) ) + 0.20 * Math.sin( Math.PI / 2 * ((t/2 + 0.5) - 5) ) - 0.27 * Math.sin( Math.PI * (t/2 + 0.5) ) - 0.09 * Math.sin( 4/7 * Math.PI * ((t/2 + 0.5) - 1) ) - 0.11 * Math.cos( 6 * Math.PI * (t/2 + 0.5) );
		const tz = t > 0.2 ? 0 : Math.pow(2.3, -(t-1)) - Math.pow(2.3, 0.8);
		
		return optionalTarget.set( tx, ty, tz ).multiplyScalar( this.scale );
	}
}

export class wirePath extends THREE.Curve {
	constructor( scale = 1 ) {
		super();
		this.scale = scale;
	}

	getPoint( t, optionalTarget = new THREE.Vector3() ) {
		const tx = 3 * t - 1.5;
		const ty = 0.16 * Math.sin( 3 * Math.PI * t ) + 0.20 * Math.sin( Math.PI / 2 * (t - 5) ) - 0.27 * Math.sin( Math.PI * t ) - 0.09 * Math.sin( 4/7 * Math.PI * (t - 1) ) - 0.11 * Math.cos( 6 * Math.PI * t );
		const tz = 0;
		
		return optionalTarget.set( tx, ty, tz ).multiplyScalar( this.scale );
	}
}
