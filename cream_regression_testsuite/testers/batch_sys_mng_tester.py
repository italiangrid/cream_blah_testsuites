import batch_sys_mng, sys

def main(argv=None):

    print "Entro nel main"

    if argv is None:
        argv = sys.argv

    batchSysFactoryLSF = batch_sys_mng.BatchSystemFactory("lsf", "cream-37.pd.infn.it", "root", "cmsgrid")
    batchSysFactoryPBS = batch_sys_mng.BatchSystemFactory("pbs", "cream-06.pd.infn.it", "root", "cmsgrid")
    print "Creo il mio lsf manager"
    batch_sys_mng_lsf = batchSysFactoryLSF.getBatchSystemMng()
    print "Creo il mio pbs manager"
    batch_sys_mng_pbs = batchSysFactoryPBS.getBatchSystemMng()


    print "Sto per cancellare il job " + argv[1]
    batch_sys_mng_lsf.del_job_from_cream_id(argv[1])
#    print "Sto per cancellare il job " + argv[1]
#    batch_sys_mng_pbs.del_job_from_cream_id(argv[1])
#    print "Sto per cancellare il job https://cream-37.pd.infn.it:8443/CREAM484620266" 
#    batch_sys_mng_lsf.del_job_from_cream_id("https://cream-37.pd.infn.it:8443/CREAM484620266")
    #print "Sto per cancellare il job " 
    #batch_sys_mng_pbs.del_job_from_cream_id("")

main()
