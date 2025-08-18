import React from 'react';

function Step2({ nextStep }) {
  return (
    <div className="step-form">
      <div className='form-title'>WE'RE LOOKING FORWARD TO YOUR UPCOMING SHOW</div>
      <p>We’ve summarised the main points to know below but you can read the full ‘How To Do A Show on RBV’ docs here:</p>
    <a href="link_to_doing_live_show_pdf">Doing a Live Show on RBV</a>
    <a href="link_to_doing_pre_recorded_show_pdf">Doing a Pre-Recorded Show on RBV</a>
    <div></div>
      <div className='form-title'>ADVANCE SOCIAL MEDIA PROMO</div>
      <b>What we do:</b>
      <ul>
        <li>Tuesday of the week of your show – we post the daily schedules for Wednesday to Sunday and tag you in them so you can share on your own socials.</li>
        <li>The day of your show – we post your individual show posts with your image/show name/ genres etc and again tag you so you can share.</li>
      </ul>

      <b>What we ask from you:</b>
      <ul>
        <li>Read through the info below</li>
        <li>Submit all the required info on the following page.</li>
      </ul>
      
      <p><b>IMPORTANT:</b> if you miss the deadline to upload your info/ image/mp3 file unfortunately it
will not be included when the socials and schedule go out/your show will not be aired. We’re
still a really small team and keeping the station running on very limited resources relies on
your help in doing the above. Your chance of future shows depends not only on the quality of
the content of your show, but also on your ability to stick to the requested deadlines, upload
required images/files/info and info and turn up on time</p>
      <div className='form-title'>FILES & FORMATTING</div>
       We recommend you put your music files through Rekordbox and double-check your USB is formatted as suggested in our info doc before arriving with your music files in mp3 or wav format only.

      <div className='form-title'>ON THE DAY</div>
      <ul>
        <li>Please turn up at least 15 mins before the start of your show.</li>
        <li>You’ll get access to get set up in the radio booth/check your USB 5 mins before
your show starts and be asked to give the same access to the host coming on
after you 5 mins before the end of your show while your last track plays out.
There will be a volunteer radio producer there to assist with any tech questions
and help get your show on and off air. Please follow their requests of when to be
in and out of the booth before and after your show and just ask them if you have
any questions at all – they are there to support you!</li>
        <li>We have a chat room you can view and use on the RBV media player on your
phone as well as a live video stream (which can be turned off if you prefer) – just
ask the volunteer for our wifi details so you can easily get online</li>
        <li>You get a 10% discount at Café Buena Vida on the day of your show.</li>
        <li>Please do not place any drinks/food on the decks or electrical equipment,
        but use the stools provided in the booth. Thank you.</li>
      </ul>

      <button className="btn" onClick={nextStep}>Next</button>
      </div>
  );
}

export default Step2;
