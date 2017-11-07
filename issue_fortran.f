! hi test
      double precision Ep,Eg
      integer reac
      do i=1,50
        Eg = 10.0**((47.0/49.0)+(2.0/49.0)*i)
        print *,i,Eg
      enddo
      do i=1,1000
        Ep = 10.0**((994.0/999.0)+(5.0/999.0)*i)
        print *,i,Ep
      enddo
      end
