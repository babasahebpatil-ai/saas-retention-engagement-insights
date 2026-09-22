"""Readable evidence charts, regenerated from analysis outputs."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

NAVY='#19354D'
TEAL='#087E8B'
ORANGE='#CD622D'
GREY='#667582'
LABELS={0:'Active-labelled',1:'Churn-labelled'}
FEATURE_NAMES={'attendance_count':'Attendance events','assessment_count':'Assessments','material_count':'Materials','teacher_count':'Teachers','student_count':'Registered students','class_count':'Classes','engagement_score':'Engagement score'}

def create_charts(root, df, quality, tables):
    sns.set_theme(style='whitegrid',font='DejaVu Sans',context='notebook')
    plt.rcParams.update({'axes.spines.top':False,'axes.spines.right':False,'axes.labelcolor':NAVY,'text.color':NAVY,'axes.titleweight':'bold','savefig.facecolor':'white','font.size':11})
    captions=[]
    def finish(fig, filename, title, subtitle, footer, source_table):
        fig.suptitle(title,x=.08,y=.97,ha='left',fontsize=19,fontweight='bold',color=NAVY)
        fig.text(.08,.885,subtitle,ha='left',fontsize=10.5,color=GREY)
        fig.text(.08,.025,footer,ha='left',va='bottom',fontsize=9,color=GREY)
        fig.savefig(root/'images'/filename,dpi=160)
        plt.close(fig)
        captions.append({'image':filename,'title':title,'subtitle':subtitle,'source_table':source_table,'note':footer})

    # 1: Show zero-heavy fields without calling zeros missing.
    q=quality[quality.column.isin(FEATURE_NAMES)].copy().sort_values('zero_share_pct')
    fig,ax=plt.subplots(figsize=(11,6.2));fig.subplots_adjust(left=.23,right=.90,top=.82,bottom=.16)
    colors=[ORANGE if x else TEAL for x in q.constant]
    ax.barh([FEATURE_NAMES[c] for c in q.column],q.zero_share_pct,color=colors,height=.62)
    for i,row in enumerate(q.itertuples()):
        ax.text(min(row.zero_share_pct+1.1,101.1),i,f'{row.zero_count:,} / {len(df):,}',va='center',fontsize=10)
    ax.set_xlim(0,125);ax.set_xticks([0,25,50,75,100]);ax.set_xlabel('Institutions with a recorded zero (%)');ax.grid(axis='y',visible=False)
    finish(fig,'01_data_quality.png','Complete fields; sparse engagement evidence',
      f'{len(df):,} institutions | 0 missing cells | orange = no variation across institutions',
      'Zero is not automatically missing. Attendance and assessment fields need source-owner verification.','data_quality.csv')

    # 2: Label distribution with arithmetic context.
    labels=tables['02_label_distribution']
    fig,ax=plt.subplots(figsize=(10,5.7));fig.subplots_adjust(left=.12,right=.94,top=.78,bottom=.20)
    ax.bar(labels.label,labels.institutions,color=[TEAL,ORANGE],width=.5)
    for i,row in enumerate(labels.itertuples()):
        ax.text(i,row.institutions+26,f'{row.institutions:,} ({row.share_pct:.1f}%)',ha='center',fontsize=14,fontweight='bold')
    ax.set_ylim(0,1250);ax.set_ylabel('Institutions');ax.grid(axis='x',visible=False)
    finish(fig,'02_churn_labels.png','A heavily imbalanced source snapshot',
      'Denominator: all 1,083 unique institutions | 0 = active; 1 = source-defined future inactivity',
      '93.9% is the supplied label share, not a monthly cancellation rate. Outcome-window dates are undisclosed.','02_label_distribution.csv')

    # 3: Positive-share comparison uses separately defined group denominators.
    e=tables['04_engagement_summary']
    selected=['student_count','teacher_count','class_count','material_count','engagement_score']
    fig,ax=plt.subplots(figsize=(11,6.5));fig.subplots_adjust(left=.23,right=.95,top=.81,bottom=.16)
    y=np.arange(len(selected));width=.34
    for label,delta,color in [(0,-width/2,TEAL),(1,width/2,ORANGE)]:
        vals=[float(e[(e.churn_label==label)&(e.metric==c)].positive_share_pct.iloc[0]) for c in selected]
        ax.barh(y+delta,vals,height=width,color=color,label=f'{LABELS[label]} (n={int(df.churn_label.eq(label).sum()):,})')
        for yi,v in zip(y+delta,vals):ax.text(v+1,yi,f'{v:.1f}%',va='center',fontsize=10)
    ax.set_yticks(y,[FEATURE_NAMES[c] for c in selected]);ax.invert_yaxis();ax.set_xlim(0,110)
    ax.set_xticks([0,25,50,75,100]);ax.set_xlabel('Institutions with a positive recorded value within each label group (%)')
    ax.legend(loc='lower right',frameon=True);ax.grid(axis='y',visible=False)
    finish(fig,'03_engagement_comparison.png','Engagement evidence differs across label groups',
      'Each bar uses its own label-group denominator; zero values remain in the analysis.',
      'Descriptive association only. Institutional size, account eligibility and the label rule may explain differences.','04_engagement_summary.csv')

    # 4: Explicit, ordered size bands rather than fitted predictive thresholds.
    segments=tables['03_student_segments']
    fig,ax=plt.subplots(figsize=(11,6));fig.subplots_adjust(left=.11,right=.96,top=.80,bottom=.22)
    ax.bar(segments.student_band,segments.churn_label_share_pct,color=[ORANGE,'#DF8C58',TEAL,NAVY],width=.58)
    for i,r in enumerate(segments.itertuples()):
        ax.text(i,r.churn_label_share_pct+2.5,f'{r.churn_label_share_pct:.1f}%\n{r.churn_labelled:,.0f} / {r.institutions:,}',ha='center',fontsize=12)
    ax.set_ylim(0,118);ax.set_yticks([0,25,50,75,100]);ax.set_ylabel('Churn-labelled share within band (%)')
    ax.set_xlabel('Registered students per institution');ax.grid(axis='x',visible=False)
    finish(fig,'04_student_segments.png','Zero-student institutions dominate churn labels',
      'Descriptive bands: 0, 1-10, 11-50, 51+ students | labels above bars show churn count / band size',
      'Bands are reporting choices, not validated risk thresholds. Larger student counts do not prove a retention effect.','03_student_segments.csv')

    # 5: Distribution evidence complements positive-share and averages.
    fig,axes=plt.subplots(1,3,figsize=(13,5.7));fig.subplots_adjust(left=.08,right=.97,top=.76,bottom=.22,wspace=.35)
    for ax,feature in zip(axes,['student_count','teacher_count','class_count']):
        dd=df[['churn_label',feature]].copy();dd['label']=dd.churn_label.map({0:'Active',1:'Churn'})
        dd['log_value']=np.log1p(dd[feature])
        sns.boxplot(data=dd,x='label',y='log_value',hue='label',order=['Active','Churn'],palette={'Active':TEAL,'Churn':ORANGE},legend=False,ax=ax,width=.5,fliersize=2)
        ticks=[0,1,5,20,100,500] if feature=='student_count' else [0,1,3,10,30]
        ax.set_yticks(np.log1p(ticks),[str(t) for t in ticks]);ax.set_ylabel(FEATURE_NAMES[feature]+' (log1p spacing)')
        ax.set_xlabel('');ax.set_title(FEATURE_NAMES[feature],fontsize=12)
        med=df.groupby('churn_label')[feature].median()
        ax.text(.5,-.23,f'Medians: active {med.loc[0]:g} | churn {med.loc[1]:g}',transform=ax.transAxes,ha='center',fontsize=10)
    finish(fig,'05_engagement_distributions.png','Institution size differs substantially',
      'Active-labelled n=66; churn-labelled n=1,017 | tick labels are original counts; log1p spacing includes zeros',
      'Quartiles and median; whiskers use 1.5 x IQR in plotted log1p space. Points lie beyond the whiskers.','04_engagement_summary.csv + data/processed/institutions_clean.csv')

    # 6: Review workloads, explicitly overlapping and not model predictions.
    groups=tables['06_review_groups'].copy()
    fig,ax=plt.subplots(figsize=(12,6.2));fig.subplots_adjust(left=.42,right=.92,top=.81,bottom=.18)
    ax.barh(groups.review_group,groups.institutions,color=[ORANGE,ORANGE,TEAL,TEAL,TEAL],height=.6)
    for i,r in enumerate(groups.itertuples()):ax.text(r.institutions+.5,i,str(r.institutions),va='center',fontsize=12)
    ax.invert_yaxis();ax.set_xlim(0,52);ax.set_xlabel('Institutions matching each review condition');ax.grid(axis='y',visible=False)
    finish(fig,'06_review_workload.png','Review the measurements before targeting customers',
      'Orange: score-definition questions | teal: active-labelled account checks',
      'Groups overlap and must not be added together. These are review flags, not predicted churn probabilities.','06_review_groups.csv')
    pd.DataFrame(captions).to_csv(root/'reports/tables/figure_index.csv',index=False)
