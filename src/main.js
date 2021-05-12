//import {OrbitControls} from '../libs/OrbitalControls.js';

var scene, renderer, camera;
var controls;

function init() {
    // create the scene. This will hold our polymers
    scene = new THREE.Scene();
    var width = window.innerWidth;
    var height = window.innerHeight;
    // create the camera, which will be used to view our polymers
    camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);

    // create RENDERER!!!
    renderer = new THREE.WebGLRenderer({antialias:true});
    renderer.setClearColor(new THREE.Color(0x1, 1.0));
    renderer.setSize(width, height);
    renderer.shadowMapEnabled = true; //not sure what this does

    document.getElementById("WebGL-output").appendChild(renderer.domElement);

    // create some axes so that we can visually orient ourselves
    var axes = new THREE.AxisHelper(10);
    scene.add(axes);

    // TODO: This is where we will create our ring-geometries from
    // output data that Python gives us.

    /* General strategy:
        1. create two arrays of vertices, with the special property 
           that the first and last vertices are the same (polygons)
        
        2. create two geometries, one for each polygon array,
           create a (special?) mesh for each polygon array geometry.
           (way to make the edges thicker, so they kind of look 
           more like polymers?)

        3. in the future:
           could interpolate curves between each point, though would 
           still end up with finite mesh. Would like smoother though
        */


    var mesh;

    var group = new THREE.Object3D();
    var chain_geometry = new THREE.Geometry();

    // from a sample run of driver.py: will be where actual data
    // goes to form the custom geometry

    chain_geometry.vertices.push(
        new THREE.Vector3(0, 0, 0),
        new THREE.Vector3(-1, 1, 1),
        new THREE.Vector3(-2, -2, -2),
        new THREE.Vector3(-1, -1, -3),
        new THREE.Vector3(-2, -2, -4),
        new THREE.Vector3(-1, -1, -5),
        new THREE.Vector3(0, 0, -4),
        new THREE.Vector3(-1, 1, -3),
        new THREE.Vector3(0, 2, -2),
        new THREE.Vector3(-1, 1, -1),
        new THREE.Vector3(0, 0, 0)
    )

    for (var j = 0; j < chain_geometry.vertices.length - 1; ++j) {
        var path = new THREE.SplineCurve3([chain_geometry.vertices[j], chain_geometry.vertices[j + 1]]);
        var tube = new THREE.TubeGeometry(path, 1, 0.04);
        var material = new THREE.MeshPhongMaterial({color: 0xcccccc});
        var mesh = new THREE.Mesh(tube, material);
        group.add(mesh);
    }

    scene.add(group);

    // position and point the camera to the center of the scene initially
    camera.position.x = 6;
    camera.position.y = 6;
    camera.position.z = 6;
    camera.lookAt(new THREE.Vector3(0, 0, 0));

    controls = new THREE.OrbitControls(camera, renderer.domElement);

    // add spotlight for the shadows
    var spotLight = new THREE.SpotLight(0xffffff);
    spotLight.position.set(-40, 60, -10);
    scene.add(spotLight);
    
    // add the output of renderer to the html element

    // // render the scene
    // renderer.render(scene, camera);
}

// this is the mesh which ig tells the renderer what to do with
// a given geometry
function createMesh(geometry) {
    var geometryMaterial = new THREE.MeshBasicMaterial({color: 0xF6DBD5, wireframe: true});
    var mesh = new THREE.Mesh(geometry, geometryMaterial);  

    return mesh;
}

function animate() {
    controls.update();
    requestAnimationFrame(animate);
    renderer.render(scene, camera);
}

init();
animate();
// // get everything running when we (re)-load the page
// window.onload = init;