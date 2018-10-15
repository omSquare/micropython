cmake_minimum_required(VERSION 3.8)

project(micropython)

add_library(micropython STATIC "")

set(__gen_dir ${CMAKE_CURRENT_BINARY_DIR}/generated)
set(__gen_qstr_src ${__gen_dir}/genhdr/qstrdefs.generated.h)

target_include_directories(micropython
        INTERFACE PUBLIC ${CMAKE_CURRENT_LIST_DIR}
        PRIVATE ports/zephyr
        PRIVATE ${__gen_dir}
        )

target_sources(micropython
        PRIVATE
        py/argcheck.c
        py/asmarm.c
        py/asmbase.c
        py/asmthumb.c
        py/asmx64.c
        py/asmx86.c
        py/asmxtensa.c
        py/bc.c
        py/binary.c
        py/builtinevex.c
        py/builtinhelp.c
        py/builtinimport.c
        py/compile.c
        py/emitbc.c
        py/emitcommon.c
        py/emitglue.c
        py/emitinlinethumb.c
        py/emitinlinextensa.c
        py/emitnarm.c
        py/emitnative.c
        py/emitnthumb.c
        py/emitnx64.c
        py/emitnx86.c
        py/emitnxtensa.c
        py/formatfloat.c
        py/frozenmod.c
        py/gc.c
        py/lexer.c
        py/malloc.c
        py/map.c
        py/modarray.c
        py/modbuiltins.c
        py/modcmath.c
        py/modcollections.c
        py/modgc.c
        py/modio.c
        py/modmath.c
        py/modmicropython.c
        py/modstruct.c
        py/modsys.c
        py/modthread.c
        py/moduerrno.c
        py/mpprint.c
        py/mpstate.c
        py/mpz.c
        py/nativeglue.c
        py/nlr.c
        py/nlrsetjmp.c
        py/nlrthumb.c
        py/nlrx64.c
        py/nlrx86.c
        py/nlrxtensa.c
        py/objarray.c
        py/objattrtuple.c
        py/objbool.c
        py/objboundmeth.c
        py/obj.c
        py/objcell.c
        py/objclosure.c
        py/objcomplex.c
        py/objdeque.c
        py/objdict.c
        py/objenumerate.c
        py/objexcept.c
        py/objfilter.c
        py/objfloat.c
        py/objfun.c
        py/objgenerator.c
        py/objgetitemiter.c
        py/objint.c
        py/objint_longlong.c
        py/objint_mpz.c
        py/objlist.c
        py/objmap.c
        py/objmodule.c
        py/objnamedtuple.c
        py/objnone.c
        py/objobject.c
        py/objpolyiter.c
        py/objproperty.c
        py/objrange.c
        py/objreversed.c
        py/objset.c
        py/objsingleton.c
        py/objslice.c
        py/objstr.c
        py/objstringio.c
        py/objstrunicode.c
        py/objtuple.c
        py/objtype.c
        py/objzip.c
        py/opmethods.c
        py/parse.c
        py/parsenumbase.c
        py/parsenum.c
        py/persistentcode.c
        py/pystack.c
        py/qstr.c
        py/reader.c
        py/repl.c
        py/runtime.c
        py/runtime_utils.c
        py/scheduler.c
        py/scope.c
        py/sequence.c
        py/showbc.c
        py/smallint.c
        py/stackctrl.c
        py/stream.c
        py/unicode.c
        py/vm.c
        py/vstr.c
        py/warning.c
        # zephyr
        ports/zephyr/
        )

add_custom_command(
        OUTPUT ${__gen_qstr_src}
        COMMAND ${CMAKE_CURRENT_LIST_DIR}/tools/cmake-qstr.py
        --compiler ${CMAKE_C_COMPILER}
        --flags \"$<TARGET_PROPERTY:micropython,COMPILE_OPTIONS>\"
        --defs \"$<TARGET_PROPERTY:micropython,COMPILE_DEFINITIONS>\"
        --includes \"$<TARGET_PROPERTY:micropython,INCLUDE_DIRECTORIES>\"
        --sources \"$<TARGET_PROPERTY:micropython,SOURCES>\"
        --outdir ${__gen_dir}/genhdr
        COMMENT "Generating QSTRs"
        DEPENDS $<TARGET_PROPERTY:micropython,SOURCES>
        VERBATIM
)

add_custom_target(micropython-generate-qstr DEPENDS ${__gen_qstr_src})
add_dependencies(micropython micropython-generate-qstr)
