#!/bin/bash

# This script is working with python 2.7 and Robot Framework trunk 20120726 (Python 2.6.8 on linux2)

test_var=`echo ${CREAM_TESTSUITE_HOME}`

if [ X == X${test_var} ]; then
    echo "CREAM_TESTSUITE_HOME not set. Please check and source testsuite_env.sh script to set the environment"
    exit 1
fi
cd ${CREAM_TESTSUITE_HOME}

# Create blah functionality tests documentation
python -m robot.testdoc blah_testing/tests/check_notifications_for_normally_finished_jobs.html blah_testing/doc/check_notifications_for_normally_finished_jobs.doc.html
python -m robot.testdoc blah_testing/tests/check_notifications_for_cancelled_jobs.html blah_testing/doc/check_notifications_for_cancelled_jobs.doc.html
python -m robot.testdoc blah_testing/tests/check_notifications_for_suspended_resumed_jobs.html blah_testing/doc/check_notifications_for_suspended_resumed_jobs.doc.html

ls -l blah_testing/doc

# Create blah regression tests documentation 
for i in `ls  blah_regression_testsuite/tests/only_new_parser/bug_*.html`; do
    src_file_name=`basename $i`
    dest_file_name=`basename $i .html`
    python -m robot.testdoc blah_regression_testsuite/tests/only_new_parser/${src_file_name} blah_regression_testsuite/doc/${dest_file_name}.doc.html
done

for i in `ls blah_regression_testsuite/tests/only_old_parser/bug_*.html`; do
    src_file_name=`basename $i`
    dest_file_name=`basename $i .html`
    python -m robot.testdoc blah_regression_testsuite/tests/only_old_parser/${src_file_name} blah_regression_testsuite/doc/${dest_file_name}.doc.html
done

ls -l blah_regression_testsuite/doc

# Create cream regression tests documentation
for i in `ls  cream_regression_testsuite/tests/bug_*.html`; do
    src_file_name=`basename $i`
    dest_file_name=`basename $i .html`
    python -m robot.testdoc cream_regression_testsuite/tests/${src_file_name} cream_regression_testsuite/doc/${dest_file_name}.doc.html
done

# Create library (lib) modules documentation
cd  ${CREAM_TESTSUITE_HOME}/doc
/usr/lib64/python2.6/pydoc.py -w cream_regression.html ${CREAM_TESTSUITE_HOME}/lib/cream_regression.py
/usr/lib64/python2.6/pydoc.py -w blah_testing.html ${CREAM_TESTSUITE_HOME}/lib/blah_testing.py
/usr/lib64/python2.6/pydoc.py -w blah_regression.html ${CREAM_TESTSUITE_HOME}/lib/blah_regression.py
/usr/lib64/python2.6/pydoc.py -w blah_regression.html ${CREAM_TESTSUITE_HOME}/lib/blah_regression.py
/usr/lib64/python2.6/pydoc.py -w cream_testsuite_exception.html ${CREAM_TESTSUITE_HOME}/lib/utils/cream_testsuite_exception.py
/usr/lib64/python2.6/pydoc.py -w batch_sys_mng.html  ${CREAM_TESTSUITE_HOME}/lib/batch_sys_mng.py 
/usr/lib64/python2.6/pydoc.py -w cream_config_layout_mng.html ${CREAM_TESTSUITE_HOME}/lib/cream_config_layout_mng.py
/usr/lib64/python2.6/pydoc.py -w submission_thread.html ${CREAM_TESTSUITE_HOME}/lib/submission_thread.py
/usr/lib64/python2.6/pydoc.py -w regression_vars.html ${CREAM_TESTSUITE_HOME}/lib/conf/regression_vars.py
/usr/lib64/python2.6/pydoc.py -w cream_testsuite_conf.html ${CREAM_TESTSUITE_HOME}/lib/conf/cream_testsuite_conf.py
/usr/lib64/python2.6/pydoc.py -w testsuite_utils.html ${CREAM_TESTSUITE_HOME}/lib/utils/testsuite_utils.py
/usr/lib64/python2.6/pydoc.py -w testsuite_exception.html ${CREAM_TESTSUITE_HOME}/lib/utils/testsuite_exception.py
/usr/lib64/python2.6/pydoc.py -w cream_testsuite_exception.html ${CREAM_TESTSUITE_HOME}/lib/utils/cream_testsuite_exception.py

