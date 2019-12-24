! systematic condition
      implicit double precision (a-h,o-z)
      integer reac
      double precision Eg,lEg,dLEg,Ep,lEp,dlEp,y,dummy,norm,gamma,gamma1
      double precision gamma2,Ebreak,mp,powerlaw,powerlaw1,powerlaw2,CHe
      double precision gammaHe,deltagammaHe,sHe,factorHe,frac,sigmafrac
      double precision dNHdR,dNHedR,dNHedR1,dNHedR2,RH,RHe,RHe0
      double precision par(4), c_a, c_b, c_c, c_d
      double precision divider, e2d, e1d, ln
      character(len=70) fn
      character(len=70) :: arg, out_file

      call spec_ini                !initialization

      reac=0                       !pp collision, combined Kamae+QGSJET
      id=0                         !photon spectrum
      sigmafrac=1.77               !fraction of crssection HeN/pN

      do i=1,iargc()
       call getarg(i,arg)
       if (i==1) then
            read(arg,*) out_file
       else
            read(arg,*) par(i-1)
       endif 
      enddo
      norm=par(1)
      gamma1=par(2)
      gamma2=par(3)
      Ebreak=par(4)
! my condition
      mp=0.938
      Nbinsg=50
      lEming=1
      lEmaxg=3
      Nbinsp=1000
      lEminp=1
      lEmaxp=6
! consequently from Eg=10**(c_a+c_b*i) !!!!
      c_b = (lEmaxg - lEming)/(Nbinsg - 1.0)
      c_a = lEming - c_b
! consequently from Ep=10**(c_c+c_d*j) !!!!
      c_d = (lEmaxp - lEminp)/(Nbinsp - 1.0)
      c_c = lEminp - c_d
! test multiple file
!      write(fn,fmt='(i0,a)') k, '.dat'
      open(2, file="./model/simdata/"//out_file)
      ! open(2,file=out_file)
! parameter
      GAMMA_PHO = 2.66
! Define powerlaw rigidity of Helium
      C=0.0948
      gammaHe=2.780
      deltagammaHe=0.119
      sHe=0.027
      RHe0=245
! start mycode
      dlEg=c_b*log(10.0)
      dlEp=c_d*log(10.0)
      EgMin=dble(10.0**lEming)
      EgMax=dble(10.0**lEmaxg)
      do i=1,Nbinsg
      !  Eg=10.0**(c_a+c_b*i)
       Eg_edge_min=EgMin*(EgMax/EgMin)**(dble(i-1)/dble(Nbinsg))
       Eg_edge_max=EgMin*(EgMax/EgMin)**(dble(i)/dble(Nbinsg))
       divider = dble(1.0 - GAMMA_PHO)
       e1d = Eg_edge_min**divider
       e2d = Eg_edge_max**divider
       ln = log((e2d - e1d)/dble(2)+ e1d)
       Eg = EXP(ln/divider)
       y=0
       do j=1,Nbinsp
        Ep=10.0**(c_c+c_d*j)
        if (Ep>Eg) then
         RH=sqrt(Ep*(Ep+2*mp))
         fff=spec_int(Ep,Eg,id,reac)
         powerlaw1=norm/(RH**gamma1)
         !(Ep*(Ep+(2.0*mp)))**(-0.5*gamma1)
         powerlaw2=(Ep+mp)/sqrt(Ep*(Ep+2.0*mp))
         powerlaw=powerlaw2*powerlaw1
         !!
         RHe=2.0*RH
         dNHedR1=C/((RHe/45.0)**(gammaHe))
         dNHedR2=(1.0+((RHe/RHe0)**(deltagammaHe/sHe)))**sHe
         dNHedR=dNHedR1*dNHedR2
         dNHdR=norm/(RH**gamma1)
         frac=sigmafrac*dNHedR*(1.0/dNHdR)*2.0
         factorHe=1.0+frac
         !!
         y=y+(Ep/Eg)*powerlaw*fff*dlEp*factorHe
        endif
       enddo
       write(2,*) Eg,y
      enddo
      close(2)
      end
