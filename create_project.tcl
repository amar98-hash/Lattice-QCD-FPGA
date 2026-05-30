# Auto-generated Vivado project script
# Project: lqcd_fpga_core

set project_name "lqcd_fpga_core"
set project_dir  "./vivado_lqcd_project"
set fpga_part    "xc7a100tcsg324-1"
set top_module   "lqcd_top"

create_project $project_name $project_dir -part $fpga_part -force

set_property target_language VHDL [current_project]
set_property simulator_language VHDL [current_project]

# -------------------------
# Add VHDL design sources
# -------------------------
set vhdl_sources [list "../src/lqcd_top.vhd" "../src/cg_core.vhd" "../src/stencil_core.vhd" "../src/fp_pipeline.vhd"]

foreach src $vhdl_sources {
    if {[file exists $src]} {
        add_files -fileset sources_1 $src
    } else {
        puts "WARNING: Missing source file: $src"
    }
}

set_property top $top_module [current_fileset]

# -------------------------
# Add simulation sources
# -------------------------
set tb_sources [list "../sim/tb_lqcd_top.vhd"]

foreach tb $tb_sources {
    if {[file exists $tb]} {
        add_files -fileset sim_1 $tb
    } else {
        puts "WARNING: Missing simulation file: $tb"
    }
}

# -------------------------
# Add constraints
# -------------------------
set xdc_files [list "../constraints/top.xdc"]

foreach xdc $xdc_files {
    if {[file exists $xdc]} {
        add_files -fileset constrs_1 $xdc
    } else {
        puts "WARNING: Missing constraint file: $xdc"
    }
}

# -------------------------
# Simulation libraries
# -------------------------
# No extra simulation libraries specified

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
