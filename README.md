# Physics Engine 3D

A simple 3D physics engine built from scratch in Python, designed for learning and extensibility.

## Goals

- Understand the math and algorithms behind physics simulations
- Build a clean, testable codebase that can scale
- Simulate rigid body dynamics, collision detection, and response

## Project Structure

physics_engine/
├── physics_math/        # Math primitives (Vector3, Matrix3)
├── core/                # Particle, RigidBody, World
├── collision/           # Detection and resolution
├── shapes/              # Sphere, Plane geometry
├── renderer/            # Visualization (moderngl + pygame)
├── tests/               # pytest test suite
└── main.py              # Entry point


## Stack

- Python 3.x
- pytest — unit testing
- moderngl + pygame — 3D rendering
- numpy — geometry data

## Setup

git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd physics_engine
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

## Running Tests

pytest -v

## Roadmap

- [x] Phase 1 — Math primitives (Vector3, Matrix3)
- [ ] Phase 2 — Particle simulation
- [ ] Phase 3 — Rigid bodies
- [ ] Phase 4 — Collision detection
- [ ] Phase 5 — Collision response
- [ ] Phase 6 — Renderer