# generate_vivado_project.py
from pathlib import Path
from textwrap import dedent

# =========================
# USER CONFIGURATION
# =========================

PROJECT_NAME = "lqcd_fpga_core"
PROJECT_DIR  = "./vivado_lqcd_project"

FPGA_PART = "xc7a100tcsg324-1"   # change this to your board/FPGA part

TOP_MODULE = "lqcd_top"

VHDL_SOURCES = [
    "src/lqcd_top.vhd",
    "src/cg_core.vhd",
    "src/stencil_core.vhd",
    "src/fp_pipeline.vhd",
]

TB_SOURCES = [
    "sim/tb_lqcd_top.vhd",
]

XDC_FILES = [
    "constraints/top.xdc",
]

SIM_LIBRARIES = [
    # add Vivado simulation libraries here if needed
    # "unisim",
    # "unimacro",
    # "secureip",
]

VIVADO_EXECUTABLE = "vivado"  # or full path to Vivado 2025 executable


# =========================
# TCL GENERATION
# =========================

def tcl_list(items):
    return " ".join(f'"{item}"' for item in items)


def generate_tcl():
    sim_lib_lines = "\n".join(
        f"set_property library {lib} [get_files -of_objects [get_filesets sim_1]]"
        for lib in SIM_LIBRARIES
    )

    return dedent(f"""
    # Auto-generated Vivado project script
    # Project: {PROJECT_NAME}

    set project_name "{PROJECT_NAME}"
    set project_dir  "{PROJECT_DIR}"
    set fpga_part    "{FPGA_PART}"
    set top_module   "{TOP_MODULE}"

    create_project $project_name $project_dir -part $fpga_part -force

    set_property target_language VHDL [current_project]
    set_property simulator_language VHDL [current_project]

    # -------------------------
    # Add VHDL design sources
    # -------------------------
    set vhdl_sources [list {tcl_list(VHDL_SOURCES)}]

    foreach src $vhdl_sources {{
        if {{[file exists $src]}} {{
            add_files -fileset sources_1 $src
        }} else {{
            puts "WARNING: Missing source file: $src"
        }}
    }}

    set_property top $top_module [current_fileset]

    # -------------------------
    # Add simulation sources
    # -------------------------
    set tb_sources [list {tcl_list(TB_SOURCES)}]

    foreach tb $tb_sources {{
        if {{[file exists $tb]}} {{
            add_files -fileset sim_1 $tb
        }} else {{
            puts "WARNING: Missing simulation file: $tb"
        }}
    }}

    # -------------------------
    # Add constraints
    # -------------------------
    set xdc_files [list {tcl_list(XDC_FILES)}]

    foreach xdc $xdc_files {{
        if {{[file exists $xdc]}} {{
            add_files -fileset constrs_1 $xdc
        }} else {{
            puts "WARNING: Missing constraint file: $xdc"
        }}
    }}

    # -------------------------
    # Simulation libraries
    # -------------------------
    {sim_lib_lines if sim_lib_lines else "# No extra simulation libraries specified"}

    # -------------------------
    # Update compile order
    # -------------------------
    update_compile_order -fileset sources_1
    update_compile_order -fileset sim_1

    # -------------------------
    # Useful runs
    # -------------------------
    puts "Vivado project generated successfully."
    puts "Project: $project_name"
    puts "Part:    $fpga_part"
    puts "Top:     $top_module"
    """).strip() + "\n"


def generate_launch_scripts():
    sh = dedent(f"""
    #!/bin/bash
    {VIVADO_EXECUTABLE} -mode batch -source create_project.tcl
    """).strip() + "\n"

    bat = dedent(f"""
    @echo off
    {VIVADO_EXECUTABLE} -mode batch -source create_project.tcl
    pause
    """).strip() + "\n"

    return sh, bat


def main():
    out_dir = Path(".")
    tcl_path = out_dir / "create_project.tcl"
    sh_path = out_dir / "run_vivado.sh"
    bat_path = out_dir / "run_vivado.bat"

    tcl_path.write_text(generate_tcl())
    sh, bat = generate_launch_scripts()
    sh_path.write_text(sh)
    bat_path.write_text(bat)

    print(f"Generated: {tcl_path}")
    print(f"Generated: {sh_path}")
    print(f"Generated: {bat_path}")


if __name__ == "__main__":
    main()