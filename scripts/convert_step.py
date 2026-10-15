import os
import re
from pathlib import Path
import gmsh
import numpy as np
import trimesh

ROOT_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = ROOT_DIR / "assets" / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

# Each model: source STEP, output GLB, mesh coarseness, and name -> color rules
MODELS = {
    "mtg": {
        "step": ROOT_DIR / "Resources" / "MTG Life Counter.step",
        "glb": MODELS_DIR / "mtg-counter.glb",
        "mesh_size_max": 4.0,
        "colors": {
            "Housing": [30, 41, 59, 255],          # Dark slate casing
            "HousingCap": [45, 55, 72, 255],       # Slate cap
            "Your_ring": [0, 210, 255, 255],       # Cyan life ring
            "Opponent_Ring": [255, 107, 0, 255],   # Orange opponent ring
            "Central_ring": [245, 158, 11, 255],   # Gold central ring
            "Knob": [15, 23, 42, 255],             # Charcoal control knob
            "Tens_shaft": [56, 189, 248, 255],     # Light blue shaft
            "Ones_Shaft": [251, 146, 60, 255],     # Amber shaft
            "TopIdler": [148, 163, 184, 255],      # Steel idler
            "BottomIdler": [148, 163, 184, 255],   # Steel idler
            "screw": [203, 213, 225, 255],         # Stainless screw
        },
    },
    "onewheel": {
        "step": ROOT_DIR / "Resources" / "OW_OneWheel.step",
        "glb": MODELS_DIR / "onewheel.glb",
        "cluster_mm": 2.5,
        "cluster_above_faces": 100000,
        "mesh_size_max": 12.0,
        "colors": {
            "Deck": [196, 160, 112, 255],          # Plywood
            "SideRail": [176, 184, 194, 255],      # Aluminum
            "Cross": [150, 158, 168, 255],         # Aluminum cross members
            "Wheel": [38, 38, 42, 255],            # Rubber
            "SPROCKET": [120, 128, 140, 255],      # Steel sprocket
            "LargeSprocket": [120, 128, 140, 255],
            "chain": [70, 74, 80, 255],            # Chain
            "CIM": [210, 214, 220, 255],           # Motor can
            "MainAxel": [90, 96, 104, 255],        # Axle
            "Bearing": [210, 180, 90, 255],        # Bearing blocks
            "SprocketBrace": [150, 158, 168, 255],
            "BoltSpacer": [203, 213, 225, 255],    # Hardware
        },
    },
}

def clean_part_name(raw_label):
    if not raw_label:
        return "Component"
    parts = raw_label.split("/")
    name = parts[-1] if parts else raw_label
    name = re.sub(r"[<>:]", "", name).strip()
    return name

def convert_step_to_glb(model_key="mtg"):
    cfg = MODELS[model_key]
    STEP_PATH, GLB_PATH, color_map = cfg["step"], cfg["glb"], cfg["colors"]
    print(f"Reading STEP file: {STEP_PATH}...")
    gmsh.initialize()
    gmsh.option.setNumber("General.Verbosity", 1)
    gmsh.option.setNumber("Mesh.MeshSizeFactor", 0.6)
    gmsh.option.setNumber("Mesh.MeshSizeMin", cfg.get("mesh_size_min", 0.5))
    gmsh.option.setNumber("Mesh.MeshSizeMax", cfg["mesh_size_max"])
    gmsh.option.setNumber("Mesh.Algorithm", 6)
    
    gmsh.model.add(model_key)
    gmsh.model.occ.importShapes(str(STEP_PATH))
    gmsh.model.occ.synchronize()

    volumes = gmsh.model.getEntities(3)
    print(f"Found {len(volumes)} volumes in CAD model.")
    
    gmsh.model.mesh.generate(2)
    
    scene = trimesh.Scene()

    processed_parts = 0
    for dim, tag in volumes:
        label = ""
        try:
            label = gmsh.model.getEntityName(dim, tag)
        except Exception:
            pass
        if not label:
            label = f"Part_{tag}"
            
        clean_name = clean_part_name(label)
        surfaces = gmsh.model.getBoundary([(dim, tag)], combined=False, oriented=False)
        
        node_coords = []
        all_nodes = {}
        triangles = []
        
        for s_dim, s_tag in surfaces:
            types, element_tags, node_tags = gmsh.model.mesh.getElements(s_dim, s_tag)
            for t_idx, elem_type in enumerate(types):
                if elem_type == 2:  # 3-node triangle
                    n_tags = node_tags[t_idx]
                    for i in range(0, len(n_tags), 3):
                        n1, n2, n3 = n_tags[i], n_tags[i+1], n_tags[i+2]
                        for n in (n1, n2, n3):
                            if n not in all_nodes:
                                res = gmsh.model.mesh.getNode(n)
                                coord = res[0]
                                all_nodes[n] = len(node_coords)
                                node_coords.append(coord)
                        triangles.append([all_nodes[n1], all_nodes[n2], all_nodes[n3]])

        if not triangles or not node_coords:
            continue

        vertices = np.array(node_coords, dtype=np.float32)
        faces = np.array(triangles, dtype=np.int32)
        
        part_mesh = trimesh.Trimesh(vertices=vertices, faces=faces, process=True)
        # Very dense parts (e.g. many-tooth sprockets) get vertex clustering: snap
        # vertices to a coarse grid and merge, which cuts triangles without a new dependency
        cluster = cfg.get("cluster_mm")
        if cluster and len(part_mesh.faces) > cfg.get("cluster_above_faces", 30000):
            part_mesh.vertices = np.round(part_mesh.vertices / cluster) * cluster
            part_mesh.merge_vertices()
            part_mesh.update_faces(part_mesh.nondegenerate_faces())
            part_mesh.update_faces(part_mesh.unique_faces())
            part_mesh.remove_unreferenced_vertices()
        
        # Assign color
        assigned_color = [180, 190, 205, 255]
        for key, col in color_map.items():
            if key.lower() in clean_name.lower() or key.lower() in label.lower():
                assigned_color = col
                break
                
        # One material color per part (much smaller GLB than per-face colors)
        part_mesh.visual = trimesh.visual.TextureVisuals(
            material=trimesh.visual.material.PBRMaterial(baseColorFactor=assigned_color))
        
        # Add to scene
        scene.add_geometry(part_mesh, node_name=f"{clean_name}_{tag}", geom_name=f"{clean_name}_{tag}")
        processed_parts += 1

    gmsh.finalize()
    print(f"Extracted {processed_parts} meshes. Exporting GLB to {GLB_PATH}...")
    
    glb_data = scene.export(file_type="glb")
    with open(GLB_PATH, "wb") as f:
        f.write(glb_data)
        
    print(f"Successfully exported {GLB_PATH.name} ({GLB_PATH.stat().st_size / 1024:.1f} KB)")

if __name__ == "__main__":
    import sys
    convert_step_to_glb(sys.argv[1] if len(sys.argv) > 1 else "mtg")
