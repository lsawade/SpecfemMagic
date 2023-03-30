
 namespace eval cfg {
    variable version 1.0

    variable sections [list DEFAULT]

    variable cursection DEFAULT
    variable DEFAULT;   # DEFAULT section
 }

 proc cfg::sections {} {
    return $cfg::sections
 }

 proc cfg::variables {{section DEFAULT}} {
    return [array names ::cfg::$section]
 }

 proc cfg::add_section {str} {
    variable sections
    variable cursection

    set cursection [string trim $str \[\]]
    if {[lsearch -exact $sections $cursection] == -1} {
      lappend sections $cursection
      variable ::cfg::${cursection}
    }
 }

 proc cfg::setvar {varname value {section DEFAULT}} {
    variable sections
    if {[lsearch -exact $sections $section] == -1} {
      cfg::add_section $section
    }
    set ::cfg::${section}($varname) $value
 }

 proc cfg::getvar {varname {section DEFAULT}} {
    variable sections
    if {[lsearch -exact $sections $section] == -1} {
      error "No such section: $section"
    }
   return [set ::cfg::${section}($varname)]
 }


 proc cfg::parse_file {filename} {
    variable sections
    variable cursection
    set line_no 1
    set fd [open $filename r]
    while {![eof $fd]} {
        set line [string trim [gets $fd] " "]
        if {$line == ""} continue
        switch -regexp -- $line {
           ^#.* { }
           ^\\[.*\\]$ {
               cfg::add_section $line
           }
           .*=.* {
               set pair [split $line =]
               set name [string trim [lindex $pair 0] " "]
               set value [string trim [lindex $pair 1] " "]
               cfg::setvar $name $value $cursection
           }
           default {
               error "Error parsing $filename (line: $line_no): $line"
           }
         }
       incr line_no
     }
     close $fd
 }

