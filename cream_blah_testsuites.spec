Summary: Regression test library and regression test suite for cream and blah
Name: cream_blah_testsuites
Version: 0.0
Release: 0
Source0: cream_blah_testsuites.tar.gz
License: GPLv3
Group: GroupName
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-buildroot
Requires: cream_test glite-ce-cream-cli python26 python26-paramiko python26-pexpect robotframework 
%description
This is the python testing module and the test suite to use
along robot framework,in order to execute a regression test
suite for CREAM and BLAH.
Documentation is also provided with this package.
%define _unpackaged_files_terminate_build 0
%prep
%setup -q
%build
%install
install -m 0755 -d $RPM_BUILD_ROOT/opt/cream_blah_testsuites
install -m 0755 -d $RPM_BUILD_ROOT/opt/cream_blah_testsuites/lib
install -m 0755 -d $RPM_BUILD_ROOT/opt/cream_blah_testsuites/lib/conf
install -m 0755 -d $RPM_BUILD_ROOT/opt/cream_blah_testsuites/lib/utils
install -m 0755 -d $RPM_BUILD_ROOT/opt/cream_blah_testsuites/doc
install -m 0755 -d $RPM_BUILD_ROOT/opt/cream_blah_testsuites/testsuites
install -m 0755 -d $RPM_BUILD_ROOT/opt/cream_blah_testsuites/testsuites/cream_regression
install -m 0755 -d $RPM_BUILD_ROOT/opt/cream_blah_testsuites/testsuites/cream_regression/tests
install -m 0755 -d $RPM_BUILD_ROOT/opt/cream_blah_testsuites/testsuites/cream_regression/doc
install -m 0755 -d $RPM_BUILD_ROOT/opt/cream_blah_testsuites/testsuites/blah_regression
install -m 0755 -d $RPM_BUILD_ROOT/opt/cream_blah_testsuites/testsuites/blah_regression/tests
install -m 0755 -d $RPM_BUILD_ROOT/opt/cream_blah_testsuites/testsuites/blah_regression/doc
install -m 0755 -d $RPM_BUILD_ROOT/opt/cream_blah_testsuites/testsuites/blah_testing
install -m 0755 -d $RPM_BUILD_ROOT/opt/cream_blah_testsuites/testsuites/blah_testing/tests
install -m 0755 -d $RPM_BUILD_ROOT/opt/cream_blah_testsuites/testsuites/blah_testing/doc
install -m 0755 testsuite_env.sh $RPM_BUILD_ROOT/opt/cream_blah_testsuites/testsuite_env.sh
install -m 0755 lib/blah_regression.py $RPM_BUILD_ROOT/opt/cream_blah_testsuites/lib/blah_regression.py
install -m 0755 lib/blah_testing.py $RPM_BUILD_ROOT/opt/cream_blah_testsuites/lib/blah_testing.py
install -m 0755 lib/cream_regression.py $RPM_BUILD_ROOT/opt/cream_blah_testsuites/lib/cream_regression.py
install -m 0755 lib/cream_config_layout_mng.py $RPM_BUILD_ROOT/opt/cream_blah_testsuites/lib/cream_config_layout_mng.py
install -m 0755 lib/batch_sys_mng.py  $RPM_BUILD_ROOT/opt/cream_blah_testsuites/lib/batch_sys_mng.py
install -m 0755 lib/submission_thread.py $RPM_BUILD_ROOT/opt/cream_blah_testsuites/lib/submission_thread.py
install -m 0755 lib/conf/cream_testsuite_conf.ini.template $RPM_BUILD_ROOT/opt/cream_blah_testsuites/lib/conf/cream_testsuite_conf.ini.template
install -m 0755 lib/conf/cream_testsuite_conf.py $RPM_BUILD_ROOT/opt/cream_blah_testsuites/lib/conf/cream_testsuite_conf.py
install -m 0755 lib/conf/regression_vars.py $RPM_BUILD_ROOT/opt/cream_blah_testsuites/lib/conf/regression_vars.py
install -m 0755 lib/utils/cream_testsuite_exception.py $RPM_BUILD_ROOT/opt/cream_blah_testsuites/lib/utils/cream_testsuite_exception.py
install -m 0755 lib/utils/testsuite_exception.py $RPM_BUILD_ROOT/opt/cream_blah_testsuites/lib/utils/testsuite_exception.py
install -m 0755 lib/utils/testsuite_utils.py $RPM_BUILD_ROOT/opt/cream_blah_testsuites/lib/utils/testsuite_utils.py
install -m 0755 cream_regression_testsuite/tests/bug_*.html $RPM_BUILD_ROOT/opt/cream_blah_testsuites/testsuites/cream_regression/tests
install -m 0755 cream_regression_testsuite/doc/bug_*.html $RPM_BUILD_ROOT/opt/cream_blah_testsuites/testsuites/cream_regression/doc
install -m 0755 blah_regression_testsuite/tests/only_new_parser/bug_*.html $RPM_BUILD_ROOT/opt/cream_blah_testsuites/testsuites/blah_regression/tests
install -m 0755 blah_regression_testsuite/tests/only_old_parser/bug_*.html $RPM_BUILD_ROOT/opt/cream_blah_testsuites/testsuites/blah_regression/tests
install -m 0755 blah_regression_testsuite/doc/bug_*.html $RPM_BUILD_ROOT/opt/cream_blah_testsuites/testsuites/blah_regression/doc
install -m 0755 blah_testing/tests/*.html $RPM_BUILD_ROOT/opt/cream_blah_testsuites/testsuites/blah_testing/tests
install -m 0755 blah_testing/doc/*.html $RPM_BUILD_ROOT/opt/cream_blah_testsuites/testsuites/blah_testing/doc
#install -m 0755 /opt/cream_blah_testsuites/docs/cream_test.7.gz
#install -m 0755 /opt/cream_blah_testsuites/docs/cream_testing_keywords.html
#install -m 0755 /opt/cream_blah_testsuites/docs/cream_testing_libdoc.html
#install -m 0755 /opt/cream_blah_testsuites/docs/Cream_Test_Suite-doc.html
#install -m 0755 docs/COPYING $RPM_BUILD_ROOT/opt/cream_blah_testsuites/docs
#install -m 0755 docs/CHANGELOG $RPM_BUILD_ROOT/opt/cream_blah_testsuites/docs
#install -m 0755 cream_test.7.gz $RPM_BUILD_ROOT/opt/cream_blah_testsuites/docs/cream_test.7.gz
#install -m 0755 cream_testing_keywords.html $RPM_BUILD_ROOT/opt/cream_blah_testsuites/docs/cream_testing_keywords.html
#install -m 0755 cream_testing_libdoc.html $RPM_BUILD_ROOT/opt/cream_blah_testsuites/docs/cream_testing_libdoc.html
#install -m 0755 Cream_Test_Suite-doc.html $RPM_BUILD_ROOT/opt/cream_blah_testsuites/docs/Cream_Test_Suite-doc.html
%clean
rm -rf $RPM_BUILD_ROOT
%post
#cp $RPM_BUILD_ROOT/opt/cream_test/docs/cream_test.7.gz /usr/share/man/man7/cream_test.7.gz
echo " "
echo "Package cream_blah_testsuites installed succesfully!"
%files
%dir /opt/cream_blah_testsuites
%dir /opt/cream_blah_testsuites/lib
%dir /opt/cream_blah_testsuites/lib/conf
%dir /opt/cream_blah_testsuites/lib/utils
%dir /opt/cream_blah_testsuites/doc
%dir /opt/cream_blah_testsuites/testsuites
%dir /opt/cream_blah_testsuites/testsuites/cream_regression
%dir /opt/cream_blah_testsuites/testsuites/cream_regression/tests
%dir /opt/cream_blah_testsuites/testsuites/cream_regression/doc
%dir /opt/cream_blah_testsuites/testsuites/blah_regression
%dir /opt/cream_blah_testsuites/testsuites/blah_regression/tests
%dir /opt/cream_blah_testsuites/testsuites/blah_regression/doc
%dir /opt/cream_blah_testsuites/testsuites/blah_testing
%dir /opt/cream_blah_testsuites/testsuites/blah_testing/tests
%dir /opt/cream_blah_testsuites/testsuites/blah_testing/doc

/opt/cream_blah_testsuites/testsuite_env.sh
/opt/cream_blah_testsuites/lib/blah_regression.py
/opt/cream_blah_testsuites/lib/blah_testing.py
/opt/cream_blah_testsuites/lib/cream_regression.py
/opt/cream_blah_testsuites/lib/cream_config_layout_mng.py
/opt/cream_blah_testsuites/lib/batch_sys_mng.py
/opt/cream_blah_testsuites/lib/submission_thread.py
/opt/cream_blah_testsuites/lib/utils/cream_testsuite_exception.py
/opt/cream_blah_testsuites/lib/utils/testsuite_exception.py
/opt/cream_blah_testsuites/lib/utils/testsuite_utils.py
/opt/cream_blah_testsuites/lib/conf/cream_testsuite_conf.ini.template
/opt/cream_blah_testsuites/lib/conf/cream_testsuite_conf.py
/opt/cream_blah_testsuites/lib/conf/regression_vars.py
/opt/cream_blah_testsuites/testsuites/cream_regression/tests/bug_*.html
/opt/cream_blah_testsuites/testsuites/cream_regression/doc/bug_*.html
/opt/cream_blah_testsuites/testsuites/blah_regression/tests/bug_*.html
/opt/cream_blah_testsuites/testsuites/blah_regression/doc/bug_*.html
/opt/cream_blah_testsuites/testsuites/blah_testing/tests/*.html
/opt/cream_blah_testsuites/testsuites/blah_testing/doc/check_notifications_for_*.html
#/opt/cream_blah_testsuites/docs/cream_test.7.gz
#/opt/cream_blah_testsuites/docs/cream_testing_keywords.html
#/opt/cream_blah_testsuites/docs/cream_testing_libdoc.html
#/opt/cream_blah_testsuites/docs/Cream_Test_Suite-doc.html
#/opt/cream_blah_testsuites/docs/COPYING
#/opt/cream_test/docs/CHANGELOG
