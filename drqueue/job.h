/* $Id: job.h,v 1.3 2001/05/30 15:11:47 jorge Exp $ */

#ifndef _JOB_H_
#define _JOB_H_

#include <stdint.h>
#include <time.h>

#include "constants.h"

typedef enum {
  JOBSTATUS_WAITING,		/* Waiting to be dispatched */
  JOBSTATUS_ACTIVE,		/* Already dispatched */
  JOBSTATUS_STOPPED,		/* Stopped, waiting for current frames to finish */
  JOBSTATUS_HSTOPPED,		/* Hard stopped, killing current frames */
  JOBSTATUS_DELETING		/* Deleting implies a hard stop and then removing */
} t_jobstatus;

typedef enum {
  FS_WAITING,			/* Waiting to be assigned */
  FS_LOADING,			/* NOT USED (yet) Assigned but not running */
  FS_ASSIGNED,			/* Currently assigned but not finished (so RUNNING) */
  FS_ERROR,			/* Finished with error */
  FS_FINISHED			/* Finished with success */
} t_framestatus;

struct frame_info {
  char status;			/* Status */
  time_t start,end;		/* Time of start and ending of the frame (32 bit integer) */
  char exitcode;		/* Exit code of the process */
  uint16_t icomp;		/* Index to computer */
  uint16_t itask;		/* Index to task on computer */
};

struct job {
  char used;
  uint16_t status;		/* Status of the job */
  char name[MAXNAMELEN];
  char cmd[MAXCMDLEN];
  char owner[MAXNAMELEN];
  uint32_t frame_start,frame_end;
  struct frame_info *frame_info; /* Status of every frame */
};

struct job;
struct database;

int job_index_free (void *pwdb);
void job_report (struct job *job);
void job_init (struct job *job);
char *job_status_string (char status);
int job_nframes (struct job *job);
int job_available (struct database *wdb,int ijob, int *iframe);
int job_first_frame_available (struct database *wdb,int ijob);
void job_update_assigned (struct database *wdb, int ijob, int iframe, int icomp, int itask);

#endif /* _JOB_H_ */
