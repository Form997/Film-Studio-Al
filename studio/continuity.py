"""Independent geometry diagnostics for supplied pose landmarks."""
from math import hypot, isfinite
from statistics import median

def validate_pose(pose):
    if not isinstance(pose, dict) or not pose or len(pose) > 100:
        raise ValueError("Pose must be a nonempty object with at most 100 joints")
    result = {}
    for key, point in pose.items():
        if not isinstance(key, str) or not key or not isinstance(point, (list, tuple)) or len(point) != 2:
            raise ValueError("Invalid joint")
        if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not isfinite(v) or not 0 <= v <= 1 for v in point):
            raise ValueError("Coordinates must be finite numbers in [0,1]")
        result[key] = (float(point[0]), float(point[1]))
    return result

def pose_distance(first, second):
    a, b = validate_pose(first), validate_pose(second)
    common = sorted(set(a) & set(b))
    if not common:
        return {"distance": None, "joint_count": 0, "status": "insufficient_data"}
    d = sum(hypot(a[k][0]-b[k][0], a[k][1]-b[k][1]) for k in common) / len(common)
    return {"distance": round(d, 6), "joint_count": len(common), "status": "measured"}

def motion_report(frames, *, jump_threshold=0.2):
    if not isinstance(frames, list) or not 2 <= len(frames) <= 10000:
        raise ValueError("Expected 2..10000 pose frames")
    if isinstance(jump_threshold, bool) or not isinstance(jump_threshold, (int, float)) or not isfinite(jump_threshold) or jump_threshold <= 0:
        raise ValueError("Invalid jump threshold")
    steps = []
    for i in range(1, len(frames)):
        item = pose_distance(frames[i-1], frames[i])
        steps.append({"from_frame": i-1, "to_frame": i, **item,
                      "possible_jump": item["distance"] is not None and item["distance"] > jump_threshold})
    measured = [s["distance"] for s in steps if s["distance"] is not None]
    return {"frame_count": len(frames), "steps": steps,
            "median_displacement": median(measured) if measured else None,
            "possible_jump_count": sum(s["possible_jump"] for s in steps),
            "unmeasured_steps": len(steps)-len(measured),
            "disclaimer": "Geometry only; no identity recognition or pose detection."}

def compare_attributes(first, second, keys=("costume", "appearance", "voice")):
    if not isinstance(first, dict) or not isinstance(second, dict):
        raise ValueError("Character records must be objects")
    changed = [k for k in keys if first.get(k) != second.get(k)]
    return {"consistent_metadata": not changed, "changed_fields": changed,
            "method": "exact_metadata_comparison"}
