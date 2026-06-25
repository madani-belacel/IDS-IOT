CONTIKI_PROJECT = clusterids-node
all: $(CONTIKI_PROJECT)

CONTIKI ?= ../../..

IDS_VARIANT ?= MAIN

unexport CPATH
unexport C_INCLUDE_PATH

GCC_SYSINC := /usr/lib/gcc/x86_64-linux-gnu/$(shell $(CC) -dumpversion)/include
ifeq ($(TARGET),cooja)
  CFLAGS += -nostdinc
  CFLAGS += -isystem $(GCC_SYSINC)
  CFLAGS += -isystem /usr/include/x86_64-linux-gnu
  CFLAGS += -isystem /usr/include
endif

CFLAGS += -include $(CURDIR)/cooja-gcc-compat.h
CFLAGS += -include $(CURDIR)/ids_conf.h

COMMON_SRC = clus_form.c ch_elect.c ids_member.c ids_ch.c ctx_policy.c \
             ids_attack.c ids_campaign_log.c

ifeq ($(IDS_VARIANT),B1)
  CFLAGS += -DIDS_VARIANT_B1=1
  CFLAGS += -imacros $(CURDIR)/variants/imacros-B1.h
  PROJECT_SOURCEFILES = $(COMMON_SRC)
else ifeq ($(IDS_VARIANT),B2)
  CFLAGS += -DIDS_VARIANT_B2=1
  CFLAGS += -imacros $(CURDIR)/variants/imacros-B2.h
  PROJECT_SOURCEFILES = $(COMMON_SRC)
else ifeq ($(IDS_VARIANT),B3)
  CFLAGS += -DIDS_VARIANT_B3=1
  CFLAGS += -imacros $(CURDIR)/variants/imacros-B3.h
  PROJECT_SOURCEFILES = $(COMMON_SRC)
else ifeq ($(IDS_VARIANT),MAIN)
  CFLAGS += -DIDS_VARIANT_MAIN=1
  CFLAGS += -imacros $(CURDIR)/variants/imacros-CLUSTERIDS.h
  PROJECT_SOURCEFILES = $(COMMON_SRC)
else ifeq ($(IDS_VARIANT),NOCLUS)
  CFLAGS += -DIDS_VARIANT_MAIN=1
  CFLAGS += -DIDS_ABLATION_NOCLUS=1
  CFLAGS += -imacros $(CURDIR)/variants/imacros-NOCLUS.h
  PROJECT_SOURCEFILES = $(COMMON_SRC)
else ifeq ($(IDS_VARIANT),MAIN_NOCLUS)
  CFLAGS += -DIDS_VARIANT_MAIN=1
  CFLAGS += -DIDS_ABLATION_NOCLUS=1
  CFLAGS += -imacros $(CURDIR)/variants/imacros-NOCLUS.h
  PROJECT_SOURCEFILES = $(COMMON_SRC)
else ifeq ($(IDS_VARIANT),NOML)
  CFLAGS += -DIDS_VARIANT_MAIN=1
  CFLAGS += -DIDS_ABLATION_NOML=1
  CFLAGS += -imacros $(CURDIR)/variants/imacros-NOML.h
  PROJECT_SOURCEFILES = $(COMMON_SRC)
else ifeq ($(IDS_VARIANT),MAIN_NOML)
  CFLAGS += -DIDS_VARIANT_MAIN=1
  CFLAGS += -DIDS_ABLATION_NOML=1
  CFLAGS += -imacros $(CURDIR)/variants/imacros-NOML.h
  PROJECT_SOURCEFILES = $(COMMON_SRC)
else ifeq ($(IDS_VARIANT),NOCTX)
  CFLAGS += -DIDS_VARIANT_MAIN=1
  CFLAGS += -DIDS_ABLATION_NOCTX=1
  CFLAGS += -imacros $(CURDIR)/variants/imacros-NOCTX.h
  PROJECT_SOURCEFILES = $(COMMON_SRC)
else ifeq ($(IDS_VARIANT),MAIN_NOCTX)
  CFLAGS += -DIDS_VARIANT_MAIN=1
  CFLAGS += -DIDS_ABLATION_NOCTX=1
  CFLAGS += -imacros $(CURDIR)/variants/imacros-NOCTX.h
  PROJECT_SOURCEFILES = $(COMMON_SRC)
else ifeq ($(IDS_VARIANT),NOENR)
  CFLAGS += -DIDS_VARIANT_MAIN=1
  CFLAGS += -DIDS_ABLATION_NOENR=1
  CFLAGS += -imacros $(CURDIR)/variants/imacros-NOENR.h
  PROJECT_SOURCEFILES = $(COMMON_SRC)
else ifeq ($(IDS_VARIANT),MAIN_NOENR)
  CFLAGS += -DIDS_VARIANT_MAIN=1
  CFLAGS += -DIDS_ABLATION_NOENR=1
  CFLAGS += -imacros $(CURDIR)/variants/imacros-NOENR.h
  PROJECT_SOURCEFILES = $(COMMON_SRC)
else
  $(error Unknown IDS_VARIANT=$(IDS_VARIANT). Use B1, B2, B3, MAIN, NOCLUS, MAIN_NOCLUS, NOML, MAIN_NOML, NOCTX, MAIN_NOCTX, NOENR, or MAIN_NOENR)
endif

ifdef IDS_CONF_CAMPAIGN_METRICS
  CFLAGS += -DIDS_CONF_CAMPAIGN_METRICS=$(IDS_CONF_CAMPAIGN_METRICS)
endif
ifdef IDS_CAMPAIGN_SEED
  CFLAGS += -DIDS_CAMPAIGN_SEED=$(IDS_CAMPAIGN_SEED)
endif
ifdef IDS_CAMPAIGN_SCENARIO
  CFLAGS += -DIDS_CAMPAIGN_SCENARIO=\"$(IDS_CAMPAIGN_SCENARIO)\"
endif

TARGET ?= cooja

include $(CONTIKI)/Makefile.include
