# 🛠️ Tangential Cutter with Python and FDM 3D Printer

Transform a standard FDM 3D printer (Artillery Sidewinder X2) into a **tangential cutting machine** using Python and DXF-based G-code generation.

## 📌 Project Overview

This project demonstrates how to repurpose a 3D printer as a **CNC tangential cutter** capable of cutting spline-based curves in thin materials (e.g., vinyl, foam). The cutting paths are defined in Fusion 360, exported as DXF files, and processed with Python to generate G-code that controls both blade orientation and movement.

> 🎓 Supervised by Prof. Dr. Başak Karpuz  
> 🏫 Dokuz Eylül University, Department of Mathematics

---


## 🧰 Technologies & Tools Used

- **Fusion 360** – CAD design and DXF export
- **Python** – Spline analysis, angle computation, G-code generation
- **ezdxf** – Reading DXF files
- **SciPy / NumPy / Matplotlib** – Geometry processing & visualization
- **Artillery Sidewinder X2** – Modified FDM printer for cutting

---

## ⚙️ Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/tangential-cutter.git
cd tangential-cutter
```

### 2. Create a Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install ezdxf
pip install numpy
pip install math
pip install scipy
pip install matplotlib.pyplot
```

---

## ▶️ Usage

### 1. Design & Export DXF

- Create your shape in **Fusion 360** as a spline. 
- Export the 2D sketch as a **DXF file** and place it in the `dxf/` folder.

### 2. Run the Python Script

```bash
python src/tangential_cutter.py dxf/yourfile.dxf
```

This will:

- Read the spline paths
- Calculate tangent angles at each point
- Generate G-code with proper blade orientation
- Save the G-code to the `output/` folder

---

## 🧪 Example Output

Here is an example G-code block:

```gcode
G92 E0.00;
G1 Z2.00 F1000.00;
G1 X10.00 Y10.00 E0.00; Cutting Spline Started
G1 Z0.00 F100.00;
G1 X20.00 Y20.00 E45.00;
...
G1 Z2.00 F1000.00; Cutting Spline Finished
```

---

## 📷 Demo

[![Watch on YouTube](https://img.youtube.com/vi/9JrX2JLhqPs/0.jpg)](https://www.youtube.com/watch?v=9JrX2JLhqPs)

---


## 📄 License

This project is open-source and available under the MIT License.

